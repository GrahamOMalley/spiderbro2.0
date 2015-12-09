import unittest
import configuration

class Test_configuration(unittest.TestCase):

    #todo configuration creates sane default config file

    def test_configuration_can_initialise_with_no_config_file(self):
        # by default tests will run in their own directory with no config file available
        conf = configuration.get_args()

    def test_configuration_has_sane_defaults(self):
        conf = configuration.get_args()
        self.assertIsNotNone(conf.tv_dir)

if __name__ == '__main__':
    unittest.main()
