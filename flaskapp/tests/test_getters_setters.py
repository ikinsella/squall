import pytest

from appname.models import db, Tag, Param, Job

@pytest.mark.usefixtures("testapp")
class TestModels:
	def test_Tag(self, testapp):
		t = Tag('tagName')
		db.session.add(t)
		db.session.commit()
		assert t.namex == 'tagName'	
		t.namex = 'blah'
		test = Tag.query.get(1)
		assert test.namex == 'blah'
		assert t.idx == 1 

 	def test_Param(self, testapp):
		p = Param('paramName', 'paramValue')
		j = Job(123)
		jj = Job(2)
		db.session.add(p)
		db.session.add(j)
		db.session.add(jj)
		db.session.commit()
		assert p.namex == 'paramName'
		assert p.valuex == 'paramValue'

		p.job_idx = jj.id
		assert p.job_idx == jj.id

		p.namex = 'newName'
		p.valuex = 'newValue'
		p.job_idx = j.id
		pq = Param.query.get(p.id)
		assert p.namex == pq.namex
		assert p.valuex == pq.valuex
		assert p.job_idx == pq.job_idx
