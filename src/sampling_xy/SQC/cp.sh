

for((i=1;i<=2000;i++))
do
  mkdir -p trajs/$i
  cp elec/traj_${i}.inp trajs/$i/trj_elec.input
  cp nuc/traj_${i}.inp trajs/$i/trj.input
done
