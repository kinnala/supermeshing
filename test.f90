module mainmod

use libsupermesh
implicit none
contains

function foo(p1, t1, p2, t2) result(b)

  use libsupermesh_intersection_finder, only : intersections, deallocate, &
    & intersection_finder
  use libsupermesh_precision, only : real_kind
  use libsupermesh_supermesh, only : intersect_elements
  use libsupermesh_tri_intersection, only : tri_type, tri_buf_size
  use libsupermesh_tet_intersection, only : tet_type, tet_buf_size
  use libsupermesh_unittest_tools, only : report_test, operator(.fne.)
  
  implicit none
  
  real(kind=8), intent(in)    :: p1(:,:)
  integer, intent(in)    :: t1(:,:)
  real(kind=8), intent(in)    :: p2(:,:)
  integer, intent(in) :: t2(:,:)
  integer, parameter :: M = 81
  real(kind=8) :: b(2 + size(p1,1), 3 * M * size(p1,2))  ! todo figure this out
  integer :: ele_a, ele_b, ele_c, i, n_tris_c
  integer, dimension(:, :), allocatable :: enlist_a, enlist_b
  ! real(kind = real_kind), dimension(2, 4) :: tri_a_real
  real(kind = real_kind) :: tri_a_real(size(p1, 1), size(t1, 1))
  ! real(kind = real_kind), dimension(2, 3, tri_buf_size) :: tris_c_real
  real(kind = real_kind) :: tris_c_real(size(p1, 1), size(t1, 1), M)
  real(kind = real_kind), dimension(:, :), allocatable :: positions_a, &
    & positions_b  
  type(intersections), dimension(:), allocatable :: map_ab
  ! type(tri_type) :: tri_a, tri_b
  type(tet_type) :: tri_a, tri_b
  ! type(tri_type), dimension(tri_buf_size) :: tris_c
  ! type(tri_type) :: tris_c(M)
  type(tet_type) :: tris_c(M)
  integer :: k
  integer :: dim
  
  dim = size(p1, 1)
  b = 0 * b
  ! print *, M * size(p1, 2)
  positions_a = p1
  enlist_a = t1
  positions_b = p2
  enlist_b = t2
  
  allocate(map_ab(size(enlist_a, 2)))
  call intersection_finder(positions_a, enlist_a, positions_b, enlist_b, map_ab)

  k = 1
  do ele_a = 1, size(enlist_a, 2)
    tri_a_real = positions_a(:, enlist_a(:, ele_a))
    do i = 1, map_ab(ele_a)%n
       ele_b = map_ab(ele_a)%v(i)
      call intersect_elements(tri_a_real, positions_b(:, enlist_b(:, ele_b)), tris_c_real, n_tris_c)
      do ele_c = 1, n_tris_c
         b(1:dim, k:(k+dim)) = tris_c_real(1:dim, 1:(dim + 1), ele_c)
         b(dim + 1, k:(k+dim)) = ele_a
         b(dim + 2, k:(k+dim)) = ele_b
         k = k + dim + 1
      end do
    end do    
 end do


  b(1, M * size(p1,2)) = k
  
  call deallocate(map_ab)
  deallocate(map_ab, positions_a, enlist_a, positions_b, enlist_b)

end function foo

end module mainmod
