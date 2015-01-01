cd /home/joereddington/topBlogs/top60auto
rm *
wget --wait 5 -i /home/joereddington/topBlogs/towget.txt
rm /home/joereddington/joereddington.com/ranking.html
cat /home/joereddington/topBlogs/start.html > /home/joereddington/joereddington.com/ranking.html
sed -n 's/.*metrics-data align-vmiddle.*\([0-9][0-9],[0-9][0-9][0-9]\).*/"disabled-world.com is ranked number \1 in the world according"/p' www.disabled-world.com  | head -n 1 > tempdisworld
grep -o -h "\"[^\"]*ranked number.*\"" * | sed 's/\"//g'  |  sed 's/\(^.*\) is ranked number\(.*\) in the.*/<\/td><td><a href=\"http:\/\/\1\">\1<\/a><\/td><td>\2<\/td><td><\/td><\/tr>/' > thelist.txt 
cat thelist.txt | sort -n -k 3 | head -n 60 > thelist2.txt
cat thelist2.txt | nl | sed 's/^/<tr><td>/g' >> /home/joereddington/joereddington.com/ranking.html
echo "</table><br> Ranking last updated at: " >> /home/joereddington/joereddington.com/ranking.html
date >> /home/joereddington/joereddington.com/ranking.html
cat /home/joereddington/topBlogs/end.html >> /home/joereddington/joereddington.com/ranking.html
