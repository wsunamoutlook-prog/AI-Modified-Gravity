1. RUN GR_gammar_masker_v3.0 for 2 scalar fields Theory Lagrangian Generation 
2. RUN EOM_v4.0 for cancelling ghost and get EOM
3. RUN Builder v4.6 for precalculation
4. RUN Solver v4.6.2 for numerical solving BAO+CC data


For SN+BAO data(in progress)

3. RUN prepare_pantheonplus to get the SN data+
4. RUN Builder v4.6 for precalculation
5. RUN Solver v5.0 for numerical solving SN+BAO data



For Random EH coefficient
3. RUN Builder v4.7 for precalculation
4. RUN Solver v4.7 for numerical solving CC+BAO data
