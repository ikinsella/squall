import pytest

from appname.models import db, Tag

@pytest.mark.usefixtures("testapp")
class TestModels:
	def test_Tag(self, testapp):
		t = Tag('tagName')
		assert t.namex == 'tagName'	
		t.namex = 'blah'
		assert t.namex == 'blah'
		assert t.idx == t.id
