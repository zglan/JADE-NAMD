        !COMPILER-GENERATED INTERFACE MODULE: Thu Jul 16 14:19:50 2015
        MODULE SUB_TRANSITION_DENSITY__genmod
          INTERFACE 
            SUBROUTINE SUB_TRANSITION_DENSITY(N_ATOM,N_AO,TRA_DENSITY1, &
     &S_AO_TO_MO,TRA_DENSITY2,S_AO_OVERLAP,BASIS)
              INTEGER(KIND=4), INTENT(IN) :: N_AO
              INTEGER(KIND=4), INTENT(IN) :: N_ATOM
              REAL(KIND=8), INTENT(IN) :: TRA_DENSITY1(N_AO,N_AO)
              REAL(KIND=8), INTENT(IN) :: S_AO_TO_MO(N_AO,N_AO)
              REAL(KIND=8), INTENT(INOUT) :: TRA_DENSITY2(N_AO,N_AO)
              REAL(KIND=8), INTENT(IN) :: S_AO_OVERLAP(N_AO,N_AO)
              INTEGER(KIND=4), INTENT(IN) :: BASIS(N_ATOM)
            END SUBROUTINE SUB_TRANSITION_DENSITY
          END INTERFACE 
        END MODULE SUB_TRANSITION_DENSITY__genmod