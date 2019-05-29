cd /home/joereddington/topBlogs/top60auto
rm *
wget --wait 5 -i /home/joereddington/topBlogs/towget.txt
python ../process_files.py > /home/joereddington/equalitytime.co.uk/rankingDis.txt
