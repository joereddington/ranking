#!/usr/bin/python
import datetime
import argparse
import glob
import os
import re

debug = False
max_dist_between_logs = 15  # in minutes
min_session_size = 15  # in minutes
vision_dir = "/Users/josephreddington/Dropbox/git/Vision/_posts/"
__TIME_FORMAT = "%d/%m/%Y-%H:%M:%S "
######################################################################
# Todo:
# The ability to recognise github commits and screenshots as input
# Output to Google Calendar!
# Given we have the timing data for each session - we can use this to import other information into the file for example
#*terminal commands/scripts
#*the desktop tracking information
######################################################################





def addEvent(cal, summary, start,end, uid):
    event = Event()
    event.add('summary', summary)
    event.add('dtstart', start)
    event.add('dtend', end)
    event.add('dtstamp', end)
    event['uid'] = summary+str(start)+str(end)
    event.add('priority', 5)

    cal.add_component(event)


class Session(object):
        project = "Unknown"
        start = ""
        end = ""

        def __init__(self, project, start, end):
                self.project, self.start, self.end = project, start, end

        def length(self):
                return self.end-self.start

        def __str__(self):
                return "    {} to {} ({})".format(
                    self.start, self.end.time(), self.length())


def setup_argument_list():
        "creates and parses the argument list for naCount"
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument(
            '-v',
            dest='verbatim',
            action='store_true',
         help='Verbose mode')
        parser.set_defaults(verbatim=False)
        parser.add_argument( '-d', dest='debug', action='store_true', help='Debugging mode')
        parser.add_argument( '-c', dest='calendar', action='store_true', help='Calendar Output')
        parser.set_defaults(debug=False)
        parser.add_argument("action", help='What to show')
        parser.add_argument("delay", nargs='?', default=0,
                            help='A delay to add in days')
        parser.add_argument(
            "context", nargs='?', default="0",
            help='The context for the action')
        parser.add_argument(
            "priority", nargs='?', default="0",
            help='From 0 to 7 how important is this action')
        return parser.parse_args()


def process_project_file(fname):
        with open(fname) as f:
                content = f.readlines()
                return process_content(content, fname)


def get_timevalues(content):
        content=[line.replace("BST","GMT") for line in content]
        timestamplines = [line for line in content
                          if "GMT" in line if "#####" in line]
        #Now remove the Unhelpful timezone from the lines and the #####
        timevalues = [line.split("GMT")[0][7:] for line in timestamplines]

        return timevalues


def ranking_from_line(line):
	match_text= '^.*#</span>(.*)'
	if re.match(match_text,line):
           a=re.match(match_text,line)
           rank= int(a.group(1).strip().replace(',',''))
           return rank
	return -1



def process_content(content, fname):
        sessions = []
        for line in content:
		ranking=ranking_from_line(line)
                if ranking>1:
		    fname=fname[:-12]
                    return (fname[39:],ranking)

        return (fname[10:], 999999999999)#If the site hasn't got a rank


def projectreport(name, sessions, verbose):
        "Produce report for one project"
        project_sessions = [
            entry for entry in sessions if (
                entry.project == name)]
        total_time = sum([entry.length()
                          for entry in project_sessions], datetime.timedelta())
        if verbose:
                print "#### {}\n\nTotal Time on this project: {}\n".format(name.ljust(45), total_time)
                for entry in project_sessions:
                        print entry
        else:
                print "{}: {}".format(name.ljust(45), total_time)
        return total_time


def all_sessions_in_folder():
        sessions = []
        for port in glob.glob("/home/joereddington/topBlogs/top60auto/*.*"):
                sessions.append(process_project_file(port))
        sessions.sort(key=lambda x: x[1])
        hope =sessions[:100]
        rank=0
        for x in hope:
            rank+=1
            print "<tr><td>{}</td><td><a href=\"http://{}\">{}</a></td><td>{:,}</td><td></td></tr>".format(rank,x[0],x[0],x[1])




def day_projects(sessions, today=datetime.datetime.today()):
        single_date_sessions = [
            entry for entry in sessions if (
                entry.start.date() == today.date())]
        total_time = sum(
            [entry.length() for entry in single_date_sessions],
            datetime.timedelta())
        projects = list(
            set([entry.project for entry in single_date_sessions]))
        for project in projects:
                projectreport(
                    project, single_date_sessions, args.verbatim)
        print "### Summary for {}\nTotal project time  -     {}".format(today.date(), total_time)


def all_projects(sessions):
        total_time = sum([entry.length()
                          for entry in sessions], datetime.timedelta())
        projects = list(set([entry.project for entry in sessions]))
        for project in projects:
                projectreport(project, sessions, args.verbatim)
        print "Total project time".ljust(45)+str(total_time)

def calendarreport(name, sessions, verbose):
        "Produce report for one project"
        project_sessions = [
            entry for entry in sessions if (
                entry.project == name)]
        total_time = sum([entry.length()
                          for entry in project_sessions], datetime.timedelta())
        for entry in project_sessions:
                add
        return total_time

def calendar_output(sessions):
    cal = Calendar()
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')
    for entry in sessions:
        addEvent(cal,entry)
    print cal.to_ical()


def addEvent(cal, entry):
    event = Event()
    event.add('summary', entry.project)
    event.add('dtstart', entry.start)
    event.add('dtend', entry.end)
    event.add('dtstamp', entry.end)
    event['uid'] = str(entry).replace(" ","")
    event.add('priority', 5)

    cal.add_component(event)


def graph_out(sesssions):
        DAY_COUNT = 7
        total_time = []
        for single_date in (
                datetime.datetime.today() - datetime.timedelta(days=n)
                for n in range(DAY_COUNT)):
                single_date_sessions = [
                    entry for entry in sessions if (
                        entry.start.date() == single_date.date())]
                element = str(int(sum([entry.length(
                        ) for entry in single_date_sessions], datetime.timedelta()).total_seconds()/60))
                total_time = [element]+total_time
        print "sessions=["+",".join(total_time)+"]"


# sessions=process_project_file(vision_dir+"2017-04-01-tmc50private.md", [])
if __name__ =="__main__":
	all_sessions_in_folder()
