subroutine sub_evolution_mapping_1_Ham_4
use mod_main
implicit none

include 'param.def'

integer i_step
real(kind=4), allocatable, dimension(:) :: x_elec
real(kind=4), allocatable, dimension(:) :: y_elec
real(kind=4), allocatable, dimension(:) :: p_x_elec
real(kind=4), allocatable, dimension(:) :: p_y_elec
double precision, allocatable, dimension(:) :: x_cur, p_cur, &
                                               x_pre, p_pre, &
                                               exci_e

double precision, allocatable, dimension(:,:) :: c_n

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

allocate ( x_elec(n_state) )
allocate ( y_elec(n_state) )
allocate ( p_x_elec(n_state) )
allocate ( p_y_elec(n_state) )
allocate (x_cur(n_mode))
allocate (p_cur(n_mode))
allocate (x_pre(n_mode))
allocate (p_pre(n_mode))
allocate (exci_e(n_state))
allocate (c_n(n_state, n_state))
allocate ( a_hamiton (n_state, n_state))
allocate (dia_hamiton(n_state, n_state))
allocate (Ham(n_state, n_state))
allocate ( lambda0(n_mode,n_state, n_state) )
allocate ( lambda1(n_mode,n_state, n_state) )
allocate (dtoa_u(n_state, n_state))
allocate (k_tun(n_state,n_mode) )
allocate (freq(n_state,n_mode))
allocate ( reduced_mass_inv_tor(n_state, n_mode_tor) )
allocate ( tor_pot_para(n_state, n_mode_tor) )

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!      
nuc_dt = nuc_dt / TOFS
!      call sub_init_random_seed()
call sub_read_ini_trj_1(label_restart,n_mode,n_state,x_cur,p_cur, &
                  x_elec, y_elec, p_x_elec, p_y_elec)
!write(*,*) 'sub_read_ini_trj_1 done!'
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

x_pre = x_cur
p_pre = p_cur
!c_n = 0.d0
!c_n(1,1) = 1.d0
do i_step=0, n_step
   
!   write(*,*) i_step
   if (mod(i_step,n_save_trj) .eq. 0 ) then
     if(label_debug >= 2 ) write(*,*) 'sub_get_dia_Ham_elec_Ham_4 begins!'
     call sub_get_dia_Ham_elec_Ham_4(x_cur, p_cur, &
                               freq, k_tun, exci_e, &
                               lambda0, lambda1, &
                               reduced_mass_inv_tor, &
                               tor_pot_para, &
                               Ham)
     !write(*,*) Ham
!     write(*,*) 'sub_get_dia_Ham_elec done!'
     !write(*,*) exci_e
     call sub_write_trj_1(i_step, &
                        x_cur, p_cur, &
                        x_elec, y_elec, &
                        p_x_elec, p_y_elec, &
                        Ham)
   endif
   
   
!         if(label_diabatic == 1)then
   call sub_elec_motion_mapping_1_Ham_4(x_cur, p_cur, &
                        x_pre, p_pre, &
                        x_elec, y_elec, &
                        p_x_elec, p_y_elec, &
                        freq, k_tun, exci_e, &
                        lambda0, lambda1, &
                        reduced_mass_inv_tor, &
                        tor_pot_para)
!   write(*,*) 'sub_elec_motion done'
!   write(*,*) x_cur
!   write(*,*) c_n
   call sub_get_c_n_elec_1(x_elec, y_elec, &
                         p_x_elec, p_y_elec, &
                         c_n)
!   write(*,*) 'sub_get_c_n_elec done'
   
!   write(*,*) x_cur
!   write(*,*) c_n
   x_pre = x_cur
   p_pre = p_cur
   call sub_nuc_motion_Ham_4( x_cur, p_cur, &
                        c_n, &
                        freq, k_tun, exci_e, &
                        lambda0, lambda1, &
                        reduced_mass_inv_tor, &
                        tor_pot_para)
!   write(*,*) 'sub_nuc_motion done'
!   write(*,*) x_cur
!   write(*,*) c_n
enddo

deallocate (x_cur)
deallocate (p_cur)
deallocate (x_pre)
deallocate (p_pre)
deallocate (c_n)


end
