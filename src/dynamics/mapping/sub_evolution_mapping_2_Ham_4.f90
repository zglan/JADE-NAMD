subroutine sub_evolution_mapping_2_Ham_4
use mod_main
implicit none

include 'param.def'

integer i_step

double precision, allocatable, dimension(:) :: x_cur, p_cur, &
                                               x_pre, p_pre, &
                                               x_elec, p_elec, &
                                               exci_e 

double precision, allocatable, dimension(:,:) :: hop_pro, c_n

complex (kind=8), allocatable, dimension(:) :: ele_coe
complex (kind=8), allocatable, dimension(:,:) :: dtoa_u
double precision, allocatable, dimension(:,:) :: a_hamiton, &
                                                dia_hamiton, &
                                                 k_tun, &
                                               freq, &
                                                Ham
double precision, allocatable, dimension(:,:,:) :: lambda0, &
                                                   lambda1
double precision, allocatable :: reduced_mass_inv_tor(:,:)
double precision, allocatable :: tor_pot_para(:,:)

allocate (x_cur(n_mode))
allocate (p_cur(n_mode))
allocate (x_pre(n_mode))
allocate (p_pre(n_mode))
allocate (x_elec(n_state))
allocate (p_elec(n_state))
allocate (exci_e(n_state))
allocate (hop_pro(n_state,n_state))
allocate (ele_coe(n_state))
allocate (c_n(n_state, n_state))
allocate ( a_hamiton (n_state, n_state))
allocate (dia_hamiton(n_state, n_state))
allocate (Ham(n_state, n_state))
allocate (dtoa_u(n_state, n_state))
allocate (freq(n_state,n_mode_HO))
allocate (k_tun(n_state,n_mode_HO) )
allocate ( lambda0(n_mode_HO,n_state, n_state) )
allocate ( lambda1(n_mode_HO,n_state, n_state) )
allocate ( reduced_mass_inv_tor(n_state, n_mode_tor) )
allocate ( tor_pot_para(n_state, n_mode_tor) )

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!      
nuc_dt = nuc_dt / TOFS
!      call sub_init_random_seed()
if(label_debug >= 2 ) write(*,*) 'sub_read_ini_trj_2 begins!'
call sub_read_ini_trj_2(x_cur, p_cur, &
                  x_elec, p_elec)
!
! vij = lambda0 + lambda1 * X
!

if(label_debug >= 2 ) write(*,*) 'sub_read_parameter_Ham_4 begins!'
call sub_read_parameter_Ham_4(freq, k_tun, exci_e, &
                    lambda0, & ! 0th parameter of vij
                    lambda1,  & ! 1th parameter of vij
                    reduced_mass_inv_tor, &
                    tor_pot_para &
                    )
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!c_n = 0.d0
!c_n(1,1) = 1.d0
x_pre = x_cur
p_pre = p_cur
if (label_aver_PES == 1) then
  do i_step=0, n_step
     
  !   write(*,*) i_step
     if ( mod(i_step,n_save_trj) .eq. 0 ) then
       if(label_debug >= 2 ) write(*,*) 'sub_get_dia_Ham_elec_Ham_4 begins!'
       call sub_get_dia_Ham_elec_Ham_4(x_cur, p_cur, &
                                 freq, k_tun, exci_e, &
                                 lambda0, lambda1, &
                                 reduced_mass_inv_tor, &
                                 tor_pot_para, &
                                 Ham)
       !write(*,*) Ham
       !write(*,*) exci_e
       if(label_debug >= 2 ) write(*,*) 'sub_write_trj_2 begins!'
       call sub_write_trj_2(i_step, &
                          x_cur, p_cur, &
                          x_elec, p_elec, &
                          Ham)
     endif
     
     
  !         if(label_diabatic == 1)then
     if(label_debug >= 2 ) write(*,*) 'sub_elec_motion_mapping_2_Ham_4_aver_PES  begins!'
     call sub_elec_motion_mapping_2_Ham_4_aver_PES(x_cur, p_cur, &
                          x_pre, p_pre, &
                          x_elec, p_elec, &
                          freq, k_tun, exci_e, &
                          lambda0, lambda1, &
                          reduced_mass_inv_tor, &
                          tor_pot_para)
  !   write(*,*) 'sub_elec_motion done'
     if(label_debug >= 2 ) write(*,*) 'sub_get_c_n_elec_2 begins!'
     call sub_get_c_n_elec_2(x_elec, p_elec, c_n)
     
     x_pre = x_cur
     p_pre = p_cur

     if(label_debug >= 2 ) write(*,*) 'sub_nuc_motion_Ham_4_aver_PES begins!'
     call sub_nuc_motion_Ham_4_aver_PES( x_cur, p_cur, &
                          c_n, &
                          freq, k_tun, exci_e, &
                          lambda0, lambda1, &
                          reduced_mass_inv_tor, &
                          tor_pot_para)
  !   write(*,*) 'sub_nuc_motion done'
  !   write(*,*) x_cur
  !   write(*,*) c_n
  enddo
else
  stop 'Now only average PES version is available for Hamtonian type 4!'
  do i_step=0, n_step
     
  !   write(*,*) i_step
     if (mod(i_step,n_save_trj) .eq. 0 ) then
       call sub_get_dia_Ham_elec(n_state, n_mode, x_cur, p_cur, &
                                 freq, k_tun, exci_e, &
                                 lambda0, lambda1, &
                                 Ham)
       !write(*,*) Ham
       !write(*,*) exci_e
       call sub_write_trj_2(i_step, &
                          x_cur, p_cur, &
                          x_elec, p_elec, &
                          Ham)
     endif
     
     
  !         if(label_diabatic == 1)then
     call sub_elec_motion_2(x_cur, p_cur, &
                          x_pre, p_pre, &
                          x_elec, p_elec, &
                          freq, k_tun, exci_e, &
                          lambda0, lambda1)
  !   write(*,*) 'sub_elec_motion done'
  !   write(*,*) x_cur
  !   write(*,*) c_n
     call sub_get_c_n_elec_2(x_elec, p_elec, c_n)
  !   write(*,*) 'sub_get_c_n_elec done'
     
  !   write(*,*) x_cur
  !   write(*,*) c_n
     x_pre = x_cur
     p_pre = p_cur
     call sub_nuc_motion( x_cur, p_cur, &
                          c_n, &
                          freq, k_tun, exci_e, &
                          lambda0, lambda1)
  !   write(*,*) 'sub_nuc_motion done'
  !   write(*,*) x_cur
  !   write(*,*) c_n
  enddo
endif

deallocate (x_cur)
deallocate (p_cur)
deallocate (x_pre)
deallocate (p_pre)
deallocate (x_elec)
deallocate (p_elec)
deallocate (ele_coe)
deallocate (hop_pro)
deallocate (c_n)
deallocate ( reduced_mass_inv_tor )
deallocate ( tor_pot_para )


end
