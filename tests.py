from django.test import TestCase
from bs4 import BeautifulSoup

class QuestionMeghodTests(TestCase):
    def test_get_text(self):
        with open('test.html') as html:
           soup = BeautifulSoup(html, 'lxml')
           print (soup.find('p').text)
           self.assertEquals(1,1)




