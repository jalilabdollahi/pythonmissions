import pytest, sys
sys.path.insert(0, ".")
from broken import IncidentSubject, SlackObserver, PagerObserver

def test_all_notified():
    subj = IncidentSubject()
    s = SlackObserver()
    p = PagerObserver()
    subj.attach(s)
    subj.attach(p)
    subj.report_incident("disk full")
    assert len(s.received) == 1
    assert len(p.received) == 1

def test_detach():
    subj = IncidentSubject()
    s = SlackObserver()
    subj.attach(s)
    subj.detach(s)
    subj.report_incident("oom")
    assert len(s.received) == 0
