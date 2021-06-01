subroutine sub_evolution_adia
use mod_main
implicit none

include 'param.def'

integer i_step

real(kind=8), allocatable, dimension(:) :: x_nuc_cur, p_nuc_cur, &
                                               x_nuc_pre, p_nuc_pre, &
                                               x_elec, p_elec, &
                                               ene_dia, ene_adia_cur, &
                                               ene_adia_pre, mass

real(kind=8), allocatable, dimension(:,:) :: hop_pro, c_n

complex(kind=8), allocatable, dimension(:) :: ele_coe
complex(kind=8), allocatable, dimension(:,:) :: dtoa_u
real(kind=8), allocatable, dimension(:,:) :: mat_U
real(kind=8), allocatable, dimension(:,:) :: a_hamiton, &
                                                dia_hamiton, &
                                                k_tun, &
                                                freq, &
                                                Ham
real(kind=8), allocatable, dimension(:,:,:) :: lambda0, &
                                               lambda1
real(kind=8), allocatable, dimension(:,:,:) :: dHmn_div_dX_adia_cur
real(kind=8), allocatable, dimension(:,:,:) :: dHmn_div_dX_adia_pre

integer i_state, i_mode

allocate (x_nuc_cur(n_mode))
allocate (p_nuc_cur(n_mode))
allocate (x_nuc_pre(n_mode))
allocate (p_nuc_pre(n_mode))
allocate (mass(n_mode))
allocate (x_elec(n_state))
allocate (p_elec(n_state))
allocate (ene_dia(n_state))
allocate (hop_pro(n_state,n_state))
allocate (ele_coe(n_state))
allocate (c_n(n_state, n_state))
allocate ( a_hamiton (n_state, n_state))
allocate (dia_hamiton(n_state, n_state))
allocate (Ham(n_state, n_state))
allocate ( lambda0(n_mode,n_state, n_state) )
allocate ( lambda1(n_mode,n_state, n_state) )
allocate ( dtoa_u(n_state, n_state) )
allocate ( mat_U(n_state, n_state) )
allocate ( k_tun(n_state,n_mode) )
allocate ( freq(n_state,n_mode) )
allocate ( ene_adia_cur(n_state) )
allocate ( ene_adia_pre(n_state) )
allocate ( dHmn_div_dX_adia_cur(n_mode, n_state, n_state) )
allocate ( dHmn_div_dX_adia_pre(n_mode, n_state, n_state) )

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!      
if(label_debug >= 2) write(*,*) 'nuc_dt', nuc_dt
nuc_dt = nuc_dt / TOFS
if(label_debug >= 2) write(*,*) 'nuc_dt', nuc_dt
!      call sub_init_random_seed()
call sub_read_ini_trj_2(x_nuc_cur, p_nuc_cur, &
                  x_elec, p_elec)
if(label_debug >= 2) then
  write(*,*) 'sub_evolution_adia'
  write(*,*) 'call sub_read_ini_trj_2 done'
  write(*,*) 'p_nuc_cur'
  do i_mode = 1, n_mode
    write(*,*) p_nuc_cur(i_mode)
  enddo
  write(*,*)
endif
!
! vij = lambda0 + lambda1 * X
!

call sub_read_parameter(freq, k_tun, ene_dia, &
                    lambda0, & ! 0th parameter of vij
                    lambda1  & ! 1th parameter of vij
                    )
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
do i_mode = 1, n_mode
  mass(i_mode) = 1.d0/freq(1,i_mode)
enddo
!c_n = 0.d0
!c_n(1,1) = 1.d0
x_nuc_pre = x_nuc_cur
p_nuc_pre = p_nuc_cur

if (label_aver_PES == 1) then
  do i_step=0, n_step
     
  !   write(*,*) i_step
!    if (mod(i_step,n_save_trj) .eq. 0 ) then
!      call sub_get_dia_Ham_elec(x_nuc_cur, p_nuc_cur, &
!                                freq, k_tun, ene_dia, &
!                                lambda0, lambda1, &
!                                Ham)
!      !write(*,*) Ham
!      !write(*,*) ene_dia
!      call sub_write_trj_2(i_step, &
!                         x_nuc_cur, p_nuc_cur, &
!                         x_elec, p_elec, &
!                         Ham)
!    endif
    
    
  !        if(label_diabatic == 1)then
    call sub_dia_to_adia(x_nuc_cur, p_nuc_cur, &
                         freq, k_tun, ene_dia, &
                         lambda0, lambda1, &
                         Ham, ene_adia_cur, &
                         dHmn_div_dX_adia_cur, &
                         mat_U)
    if(label_debug >= 2) then
      write(*,*) 'sub_evolution_adia'
      write(*,*) 'call sub_dia_to_adia done'
      write(*,*) 'p_nuc_cur'
      do i_mode = 1, 2 !n_mode
        write(*,*) p_nuc_cur(i_mode)
      enddo
      write(*,*)
    endif

    if(label_debug >= 2) then
      write(*,*) 'i_step:', i_step
      write(*,*) 'sub_evolution_adia'
      write(*,*) 'call sub_dia_to_adia done'
      write(*,*) 'd12:'
      do i_mode = 1, 2 !n_mode
        write(*,*) dHmn_div_dX_adia_cur(i_mode,1,2)
      enddo
      write(*,*)
    endif
    
    
    if (mod(i_step,n_save_trj) .eq. 0 ) then
      call sub_write_trj_2_adia(i_step, &
                         x_elec, p_elec, &
                         x_nuc_cur, p_nuc_cur, &
                         mat_U)
    endif
    
    if (i_step == 0) then
      ene_adia_pre = ene_adia_cur
      dHmn_div_dX_adia_pre = dHmn_div_dX_adia_cur
    endif
    call sub_motion_2_adia_aver_PES_1step(x_elec, &
                         p_elec, &
                         x_nuc_cur, &
                         p_nuc_cur, &
                         ene_adia_cur, &
                         dHmn_div_dX_adia_cur, &
                         mass, &
                         x_nuc_pre, &
                         p_nuc_pre, &
                         ene_adia_pre, &
                         dHmn_div_dX_adia_pre)
  enddo
else
  write(*,*) "Non-aver-pes subroutine is not available now!"
endif

deallocate (x_nuc_cur)
deallocate (p_nuc_cur)
deallocate (x_nuc_pre)
deallocate (p_nuc_pre)
deallocate (x_elec)
deallocate (p_elec)
deallocate (ele_coe)
deallocate (hop_pro)
deallocate (c_n)


end
