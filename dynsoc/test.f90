!
!
!   this is a test version of the main program
!   simplely used for add new feature
       integer :: file_dynvar_in


       integer :: i, j, it, i_state
       integer :: ntime, n_sav_stat, n_sav_traj
       integer :: n_state, ntime_ele
       
       integer :: qm_method, dyn_method
  
!       integer, allocatable, dimension(:) ::  md_state
       integer, allocatable, dimension(:) ::  md_state_list


       double precision :: time,  dtime, cor_dec
       integer :: seed_random
 
       integer :: label_read_velocity
       integer :: label_nac_phase      
       integer :: label_reject_hops
       integer :: label_restart
       double precision ::   hop_e   
        integer id
       complex (kind=8), allocatable, dimension(:, :) :: rho
       integer :: index_state
!       character (len=100) md_state
        
        namelist /control/ dyn_method, ntime, dtime, n_sav_stat, n_sav_traj, ntime_ele, &
            qm_package, qm_method, n_state, md_state, i_state, &
            seed_random, cor_dec, label_nac_phase, label_reject_hops, hop_e, &
            label_read_velocity, label_restart
            
            
       write (*,*) "Initialization"
       file_dynvar_in=21       
       open(unit=file_dynvar_in, file="dyn.inp")
       read(file_dynvar_in, nml = control)
       write(*,*)  n_state, md_state
       close(file_dynvar_in)
      ! allocate (md_state(n_state))
       
      ! read(md_state, *) (md_state_int(i),i=1,n_state)
      ! write(*,*) md_state_int, n_state
       write(*,nml=control) 
       end
       
       
       
       
                   
