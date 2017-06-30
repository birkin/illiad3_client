import os, sys, unittest

## add project parent-directory to sys.path
parent_working_dir = os.path.abspath( os.path.join(os.getcwd(), os.pardir) )
sys.path.append( parent_working_dir )

from illiad3_client.illiad3 import parsers


#Directory where test data is stored.
DATA_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'data'
    )


class ParserTest(unittest.TestCase):

    def test_login(self):
        path = os.path.join(DATA_PATH, 'login.html')
        with open( path, 'rt' ) as f:
            content = f.read()
        login = parsers.main_menu(content)
        self.assertTrue(login['authenticated'])
        self.assertEqual(login['session_id'],
                         'Q102112146D')

    def test_needs_registration(self):
        path = os.path.join(DATA_PATH, 'not_registered.html')
        with open( path, 'rt' ) as f:
            content = f.read()
        login = parsers.main_menu(content)
        self.assertFalse(login['registered'])

    def test_article_request_key(self):
        """
        Test a few values for an article request key.
        """
        def _key_check(key_list, rdict):
            for k in key_list:
                self.assertTrue(k in rdict,
                                msg="Request key missing key -- %s." % k)
        path = os.path.join(DATA_PATH, 'article_request.html')
        with open( path, 'rt' ) as f:
            content = f.read()
        self.assertEqual( str, type(content) )  # content is unicode
        submit_details = parsers.request_form(content)
        request_key = submit_details
        _key_check(['PhotoJournalInclusivePages',
                    'PhotoJournalYear',
                    'PhotoJournalTitle'],
                   request_key)
        jtitle = request_key.get('PhotoJournalTitle')
        self.assertEqual(jtitle,
                         'Current pharmaceutical design')
        atitle = request_key.get('PhotoArticleTitle')
        self.assertTrue(u'Nicotinic Acetylcholine Receptors' in atitle)
        issn = request_key.get('ISSN')
        self.assertEqual(issn,
                         u'1381-6128')

    def test_blocked_patron(self):
        path = os.path.join(DATA_PATH, 'blocked.html')
        with open( path, 'rt' ) as f:
            content = f.read()
        request_key = parsers.request_form(content)
        self.assertTrue(request_key['blocked'])
        blocked_found = request_key['errors'].rfind('blocked')
        self.assertNotEqual(blocked_found, -1)

    def test_completed_request_submission(self):
        path = os.path.join(DATA_PATH, 'completed_request.html')
        with open( path, 'rt' ) as f:
            content = f.read()
        submit = parsers.request_submission(content)
        self.assertFalse(submit['error'])
        self.assertEqual(
            submit['transaction_number'],
            '476993'
        )
        self.assertTrue(submit['submitted'])

    def test_failed_request_submission(self):
        path = os.path.join(DATA_PATH, 'failed_request_missing_field.html')
        with open( path, 'rt' ) as f:
            content = f.read()
        submit = parsers.request_submission(content)
        self.assertTrue(submit['error'])
        self.assertEqual(submit['message'],
                         'Photo Journal Year is a required field.')


def suite():
    suite = unittest.makeSuite(ParserTest, 'test')
    return suite

if __name__ == '__main__':
    unittest.main()
