import argparse
import json
import math
import os
import random
import tempfile
import unittest
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from typing import DefaultDict, Dict, List, Optional, Tuple

# ============================================================
# 1. CONFIG
# ============================================================


@dataclass
class Config:
    # data
    train_path: str = "train_sequences.jsonl"
    val_path: str = "val_sequences.jsonl"
    max_seq_len: int = 128
    min_freq: int = 1

    # model
    ngram_order: int = 3  # 1=unigram, 2=bigram, 3=trigram
    smoothing_alpha: float = 0.5

    # runtime
    seed: int = 42
    save_path: str = "tensor_ngram_model.json"
    vocab_path: str = "vocab.json"


CFG = Config()


# ============================================================
# 2. UTILS
# ============================================================


def set_seed(seed: int) -> None:
    random.seed(seed)


# ============================================================
# 3. VOCAB
# ============================================================


class Vocab:
    PAD = "<pad>"
    BOS = "<bos>"
    EOS = "<eos>"
    UNK = "<unk>"

    def __init__(self, token_to_id: Dict[str, int]):
        self.token_to_id = token_to_id
        self.id_to_token = {i: t for t, i in token_to_id.items()}

    @classmethod
    def build(cls, sequences: List[List[str]], min_freq: int = 1) -> "Vocab":
        freq: Dict[str, int] = {}
        for seq in sequences:
            for tok in seq:
                freq[tok] = freq.get(tok, 0) + 1

        tokens = [cls.PAD, cls.BOS, cls.EOS, cls.UNK]
        tokens += sorted(tok for tok, c in freq.items() if c >= min_freq and tok not in tokens)
        token_to_id = {tok: i for i, tok in enumerate(tokens)}
        return cls(token_to_id)

    def encode(self, tokens: List[str], add_bos: bool = True, add_eos: bool = True) -> List[int]:
        ids: List[int] = []
        if add_bos:
            ids.append(self.token_to_id[self.BOS])
        unk_id = self.token_to_id[self.UNK]
        ids.extend(self.token_to_id.get(tok, unk_id) for tok in tokens)
        if add_eos:
            ids.append(self.token_to_id[self.EOS])
        return ids

    def decode(self, ids: List[int], skip_special: bool = True) -> List[str]:
        out: List[str] = []
        specials = {self.PAD, self.BOS, self.EOS}
        for idx in ids:
            tok = self.id_to_token.get(idx, self.UNK)
            if skip_special and tok in specials:
                continue
            out.append(tok)
        return out

    @property
    def pad_id(self) -> int:
        return self.token_to_id[self.PAD]

    @property
    def bos_id(self) -> int:
        return self.token_to_id[self.BOS]

    @property
    def eos_id(self) -> int:
        return self.token_to_id[self.EOS]

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.token_to_id, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path: str) -> "Vocab":
        with open(path, "r", encoding="utf-8") as f:
            token_to_id = json.load(f)
        return cls(token_to_id)

    def __len__(self) -> int:
        return len(self.token_to_id)


# ============================================================
# 4. DATA FORMAT
# ============================================================
# Expected JSONL format:
# {"tokens": ["ADD", "R", "Ricci2"]}
# or
# {"tokens": ["Ricci_dd", "Ricci_dd", "metric_uu", "metric_uu"]}
# ============================================================


def load_jsonl_sequences(path: str) -> List[List[str]]:
    sequences: List[List[str]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if "tokens" not in obj or not isinstance(obj["tokens"], list):
                raise ValueError(f"Each line must contain a list under key 'tokens'. Bad line: {line[:120]}")
            if not all(isinstance(tok, str) for tok in obj["tokens"]):
                raise ValueError(f"All tokens must be strings. Bad line: {line[:120]}")
            sequences.append(obj["tokens"])
    return sequences


def truncate_sequence(ids: List[int], max_seq_len: int, eos_id: int) -> List[int]:
    if len(ids) <= max_seq_len:
        return ids
    truncated = ids[: max_seq_len - 1] + [eos_id]
    return truncated


# ============================================================
# 5. N-GRAM LANGUAGE MODEL
# ============================================================


class NGramLanguageModel:
    """
    Standard-library-only language model used as a drop-in replacement for the
    original PyTorch-based transformer in environments where torch is unavailable.

    It learns p(next_token | previous n-1 tokens) with additive smoothing.
    """

    def __init__(self, vocab_size: int, ngram_order: int = 3, smoothing_alpha: float = 0.5):
        if ngram_order < 1:
            raise ValueError("ngram_order must be >= 1")
        if smoothing_alpha <= 0:
            raise ValueError("smoothing_alpha must be > 0")
        self.vocab_size = vocab_size
        self.ngram_order = ngram_order
        self.smoothing_alpha = smoothing_alpha
        self.context_counts: DefaultDict[Tuple[int, ...], Counter] = defaultdict(Counter)
        self.total_context_counts: Counter = Counter()
        self.unigram_counts: Counter = Counter()
        self.total_unigrams: int = 0

    def fit(self, encoded_sequences: List[List[int]]) -> None:
        self.context_counts = defaultdict(Counter)
        self.total_context_counts = Counter()
        self.unigram_counts = Counter()
        self.total_unigrams = 0

        for seq in encoded_sequences:
            for tok in seq:
                self.unigram_counts[tok] += 1
                self.total_unigrams += 1

            for i in range(len(seq)):
                token = seq[i]
                max_ctx = min(self.ngram_order - 1, i)
                for ctx_len in range(max_ctx, -1, -1):
                    context = tuple(seq[i - ctx_len : i])
                    self.context_counts[context][token] += 1
                    self.total_context_counts[context] += 1

    def _best_context(self, context: List[int]) -> Tuple[int, ...]:
        max_len = min(len(context), self.ngram_order - 1)
        for ctx_len in range(max_len, -1, -1):
            candidate = tuple(context[-ctx_len:]) if ctx_len > 0 else tuple()
            if candidate in self.context_counts:
                return candidate
        return tuple()

    def next_token_distribution(self, context: List[int]) -> Dict[int, float]:
        ctx = self._best_context(context)
        token_counter = self.context_counts.get(ctx, Counter())
        total = self.total_context_counts.get(ctx, 0)
        alpha = self.smoothing_alpha
        denom = total + alpha * self.vocab_size
        return {
            tok_id: (token_counter.get(tok_id, 0) + alpha) / denom
            for tok_id in range(self.vocab_size)
        }

    def sequence_nll(self, seq: List[int]) -> float:
        nll = 0.0
        for i in range(1, len(seq)):
            context = seq[:i]
            dist = self.next_token_distribution(context)
            prob = max(dist.get(seq[i], 0.0), 1e-15)
            nll -= math.log(prob)
        return nll

    def average_loss(self, encoded_sequences: List[List[int]]) -> float:
        total_nll = 0.0
        total_predictions = 0
        for seq in encoded_sequences:
            if len(seq) < 2:
                continue
            total_nll += self.sequence_nll(seq)
            total_predictions += len(seq) - 1
        if total_predictions == 0:
            return 0.0
        return total_nll / total_predictions

    def sample_next_token(
        self,
        context: List[int],
        rng: random.Random,
        temperature: float = 1.0,
        top_k: Optional[int] = None,
    ) -> int:
        if temperature <= 0:
            raise ValueError("temperature must be > 0")

        dist = self.next_token_distribution(context)
        items = list(dist.items())

        if top_k is not None and top_k > 0:
            items.sort(key=lambda x: x[1], reverse=True)
            items = items[: min(top_k, len(items))]

        if temperature != 1.0:
            adjusted = []
            for tok_id, prob in items:
                adjusted.append((tok_id, prob ** (1.0 / temperature)))
            items = adjusted

        total = sum(prob for _, prob in items)
        if total <= 0:
            return 0
        threshold = rng.random() * total
        cumulative = 0.0
        for tok_id, prob in items:
            cumulative += prob
            if cumulative >= threshold:
                return tok_id
        return items[-1][0]

    def generate(
        self,
        input_ids: List[int],
        max_new_tokens: int,
        eos_id: Optional[int] = None,
        temperature: float = 1.0,
        top_k: Optional[int] = None,
        seed: int = 42,
    ) -> List[int]:
        rng = random.Random(seed)
        output = list(input_ids)
        for _ in range(max_new_tokens):
            next_id = self.sample_next_token(output, rng, temperature=temperature, top_k=top_k)
            output.append(next_id)
            if eos_id is not None and next_id == eos_id:
                break
        return output

    def to_dict(self) -> Dict[str, object]:
        serialized_context_counts = {
            "|".join(map(str, context)): dict(counter)
            for context, counter in self.context_counts.items()
        }
        serialized_total_context_counts = {
            "|".join(map(str, context)): total
            for context, total in self.total_context_counts.items()
        }
        return {
            "vocab_size": self.vocab_size,
            "ngram_order": self.ngram_order,
            "smoothing_alpha": self.smoothing_alpha,
            "context_counts": serialized_context_counts,
            "total_context_counts": serialized_total_context_counts,
            "unigram_counts": dict(self.unigram_counts),
            "total_unigrams": self.total_unigrams,
        }

    @classmethod
    def from_dict(cls, payload: Dict[str, object]) -> "NGramLanguageModel":
        model = cls(
            vocab_size=int(payload["vocab_size"]),
            ngram_order=int(payload["ngram_order"]),
            smoothing_alpha=float(payload["smoothing_alpha"]),
        )
        context_counts_raw = payload.get("context_counts", {})
        total_context_counts_raw = payload.get("total_context_counts", {})

        model.context_counts = defaultdict(Counter)
        for context_key, counts in context_counts_raw.items():
            context = tuple(int(x) for x in context_key.split("|") if x != "")
            model.context_counts[context] = Counter({int(k): int(v) for k, v in counts.items()})

        model.total_context_counts = Counter()
        for context_key, total in total_context_counts_raw.items():
            context = tuple(int(x) for x in context_key.split("|") if x != "")
            model.total_context_counts[context] = int(total)

        model.unigram_counts = Counter({int(k): int(v) for k, v in payload.get("unigram_counts", {}).items()})
        model.total_unigrams = int(payload.get("total_unigrams", 0))
        return model

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path: str) -> "NGramLanguageModel":
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        return cls.from_dict(payload)


# ============================================================
# 6. TRAIN / EVAL
# ============================================================


def prepare_encoded_sequences(sequences: List[List[str]], vocab: Vocab, max_seq_len: int) -> List[List[int]]:
    encoded: List[List[int]] = []
    for seq in sequences:
        ids = vocab.encode(seq, add_bos=True, add_eos=True)
        ids = truncate_sequence(ids, max_seq_len=max_seq_len, eos_id=vocab.eos_id)
        encoded.append(ids)
    return encoded


def perplexity_from_loss(loss: float) -> float:
    return math.exp(min(loss, 50.0))


def train_model(train_sequences: List[List[int]], cfg: Config, vocab_size: int) -> NGramLanguageModel:
    model = NGramLanguageModel(
        vocab_size=vocab_size,
        ngram_order=cfg.ngram_order,
        smoothing_alpha=cfg.smoothing_alpha,
    )
    model.fit(train_sequences)
    return model


def evaluate_model(model: NGramLanguageModel, sequences: List[List[int]]) -> Tuple[float, float]:
    loss = model.average_loss(sequences)
    ppl = perplexity_from_loss(loss)
    return loss, ppl


# ============================================================
# 7. MAIN TRAINING ENTRY
# ============================================================


def main_train() -> None:
    set_seed(CFG.seed)

    print("Loading data...")
    train_sequences_raw = load_jsonl_sequences(CFG.train_path)
    val_sequences_raw = load_jsonl_sequences(CFG.val_path)

    print(f"Train examples (raw): {len(train_sequences_raw)}")
    print(f"Val examples (raw):   {len(val_sequences_raw)}")

    vocab = Vocab.build(train_sequences_raw, min_freq=CFG.min_freq)
    vocab.save(CFG.vocab_path)
    print(f"Vocab size: {len(vocab)}")

    train_sequences = prepare_encoded_sequences(train_sequences_raw, vocab, CFG.max_seq_len)
    val_sequences = prepare_encoded_sequences(val_sequences_raw, vocab, CFG.max_seq_len)

    model = train_model(train_sequences, CFG, len(vocab))

    train_loss, train_ppl = evaluate_model(model, train_sequences)
    val_loss, val_ppl = evaluate_model(model, val_sequences)

    print(
        f"Training complete | train loss {train_loss:.4f} | train ppl {train_ppl:.2f} | "
        f"val loss {val_loss:.4f} | val ppl {val_ppl:.2f}"
    )

    payload = {
        "config": asdict(CFG),
        "model": model.to_dict(),
    }
    with open(CFG.save_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"Saved model to {CFG.save_path}")


# ============================================================
# 8. SAMPLING / INFERENCE
# ============================================================


def load_model_and_vocab(checkpoint_path: str, vocab_path: str) -> Tuple[NGramLanguageModel, Vocab, Config]:
    vocab = Vocab.load(vocab_path)
    with open(checkpoint_path, "r", encoding="utf-8") as f:
        ckpt = json.load(f)
    cfg = Config(**ckpt["config"])
    model = NGramLanguageModel.from_dict(ckpt["model"])
    return model, vocab, cfg


def sample_expression(
    checkpoint_path: str,
    vocab_path: str,
    prompt_tokens: Optional[List[str]] = None,
    max_new_tokens: int = 40,
    temperature: float = 1.0,
    top_k: Optional[int] = 20,
    seed: int = 42,
) -> List[str]:
    model, vocab, _ = load_model_and_vocab(checkpoint_path, vocab_path)

    prompt_tokens = prompt_tokens or []
    input_ids = vocab.encode(prompt_tokens, add_bos=True, add_eos=False)

    out_ids = model.generate(
        input_ids=input_ids,
        max_new_tokens=max_new_tokens,
        eos_id=vocab.eos_id,
        temperature=temperature,
        top_k=top_k,
        seed=seed,
    )

    tokens = vocab.decode(out_ids, skip_special=True)
    print("Generated tokens:")
    print(tokens)
    return tokens


# ============================================================
# 9. OPTIONAL: SYNTHETIC DATA GENERATOR FOR STAGE 1
# ============================================================
# This helper creates toy data from your Stage-1 index-signature grammar.
# It is NOT a full physics generator; it only creates coarse candidates with U=D.
# ============================================================

TOKEN_SIGNATURES: Dict[str, Tuple[int, int]] = {
    "R": (0, 0),
    "Ricci_dd": (0, 2),
    "Riemann_dddd": (0, 4),
    "metric_uu": (2, 0),
    "metric_dd": (0, 2),
    "eps_uuuu": (4, 0),
    "eps_dddd": (0, 4),
    "dphi_d": (0, 1),
    "ddphi_dd": (0, 2),
    "Weyl_dddd": (0, 4),
}


def generate_stage1_candidate(max_terms: int = 5, max_trials: int = 200) -> Optional[List[str]]:
    tokens = list(TOKEN_SIGNATURES.keys())
    for _ in range(max_trials):
        n = random.randint(1, max_terms)
        seq = [random.choice(tokens) for _ in range(n)]
        up = sum(TOKEN_SIGNATURES[t][0] for t in seq)
        down = sum(TOKEN_SIGNATURES[t][1] for t in seq)
        if up == down:
            return seq
    return None


def write_toy_dataset(path: str, n_examples: int = 1000) -> None:
    with open(path, "w", encoding="utf-8") as f:
        written = 0
        while written < n_examples:
            seq = generate_stage1_candidate()
            if seq is None:
                continue
            f.write(json.dumps({"tokens": seq}, ensure_ascii=False) + "\n")
            written += 1
    print(f"Wrote {written} examples to {path}")


# ============================================================
# 10. TESTS
# ============================================================


class TestVocab(unittest.TestCase):
    def test_encode_decode_roundtrip(self) -> None:
        sequences = [["R", "Ricci_dd"], ["metric_uu"]]
        vocab = Vocab.build(sequences)
        ids = vocab.encode(["R", "metric_uu"])
        decoded = vocab.decode(ids)
        self.assertEqual(decoded, ["R", "metric_uu"])

    def test_unknown_token_maps_to_unk(self) -> None:
        vocab = Vocab.build([["R"]])
        ids = vocab.encode(["NOT_IN_VOCAB"], add_bos=False, add_eos=False)
        self.assertEqual(ids, [vocab.token_to_id[Vocab.UNK]])


class TestDataUtilities(unittest.TestCase):
    def test_truncate_sequence_ends_with_eos(self) -> None:
        eos_id = 2
        seq = [1, 5, 6, 7, 8]
        truncated = truncate_sequence(seq, max_seq_len=4, eos_id=eos_id)
        self.assertEqual(truncated, [1, 5, 6, eos_id])

    def test_load_jsonl_sequences(self) -> None:
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as tmp:
            tmp.write(json.dumps({"tokens": ["R", "Ricci_dd"]}) + "\n")
            tmp.write(json.dumps({"tokens": ["metric_uu"]}) + "\n")
            path = tmp.name
        try:
            loaded = load_jsonl_sequences(path)
            self.assertEqual(loaded, [["R", "Ricci_dd"], ["metric_uu"]])
        finally:
            os.remove(path)


class TestNGramLanguageModel(unittest.TestCase):
    def test_distribution_sums_to_one(self) -> None:
        model = NGramLanguageModel(vocab_size=5, ngram_order=2, smoothing_alpha=0.5)
        model.fit([[1, 2, 3], [1, 2, 4]])
        dist = model.next_token_distribution([1, 2])
        self.assertAlmostEqual(sum(dist.values()), 1.0, places=9)

    def test_seen_transition_more_likely_than_unseen(self) -> None:
        model = NGramLanguageModel(vocab_size=6, ngram_order=2, smoothing_alpha=0.5)
        model.fit([[1, 2, 3], [1, 2, 3], [1, 2, 4]])
        dist = model.next_token_distribution([1, 2])
        self.assertGreater(dist[3], dist[5])

    def test_generate_returns_prompt_prefix(self) -> None:
        model = NGramLanguageModel(vocab_size=6, ngram_order=2, smoothing_alpha=0.5)
        model.fit([[1, 2, 3], [1, 2, 4]])
        prompt = [1, 2]
        generated = model.generate(prompt, max_new_tokens=3, eos_id=None, seed=7)
        self.assertEqual(generated[: len(prompt)], prompt)
        self.assertGreaterEqual(len(generated), len(prompt))


class TestToyData(unittest.TestCase):
    def test_generate_stage1_candidate_balances_indices(self) -> None:
        seq = generate_stage1_candidate(max_terms=6, max_trials=500)
        self.assertIsNotNone(seq)
        assert seq is not None
        up = sum(TOKEN_SIGNATURES[t][0] for t in seq)
        down = sum(TOKEN_SIGNATURES[t][1] for t in seq)
        self.assertEqual(up, down)


# ============================================================
# 11. CLI
# ============================================================


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, required=True, choices=["train", "sample", "make_toy_data", "test"])
    parser.add_argument("--prompt", type=str, default="")
    parser.add_argument("--checkpoint", type=str, default=CFG.save_path)
    parser.add_argument("--vocab", type=str, default=CFG.vocab_path)
    parser.add_argument("--out", type=str, default="train_sequences.jsonl")
    parser.add_argument("--n_examples", type=int, default=1000)
    parser.add_argument("--max_new_tokens", type=int, default=40)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--top_k", type=int, default=20)
    parser.add_argument("--seed", type=int, default=CFG.seed)
    args = parser.parse_args()

    if args.mode == "train":
        main_train()
    elif args.mode == "sample":
        prompt_tokens = args.prompt.split() if args.prompt.strip() else []
        sample_expression(
            checkpoint_path=args.checkpoint,
            vocab_path=args.vocab,
            prompt_tokens=prompt_tokens,
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
            top_k=args.top_k,
            seed=args.seed,
        )
    elif args.mode == "make_toy_data":
        write_toy_dataset(args.out, n_examples=args.n_examples)
    elif args.mode == "test":
        unittest.main(argv=["ignored"], exit=False)


if __name__ == "__main__":
    main()
