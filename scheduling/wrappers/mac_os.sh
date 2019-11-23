export PATH=$PATH:$1
cd $2
python3 $2/scheduler.py --f $3
