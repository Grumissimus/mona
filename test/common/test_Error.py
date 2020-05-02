import unittest
import sys
sys.path.append('../../mona/')
from mona.common.error import Error, ErrorType, ErrorMessageBuilder, ErrorFactory


class TestError(unittest.TestCase):
    def test_error_set_up(self):
        errType = ErrorType.Unknown
        errMsg = "Test Error Message"
        err = Error(errType, errMsg)

        self.assertIsInstance(err, Error)
        self.assertEqual(err.errorType, errType)
        self.assertEqual(err.message, errMsg)

    def test_error_builder(self):
        rowline = 1
        colline = 1
        errType = ErrorType.Unknown
        msg = "Error message"

        errMsg = ErrorMessageBuilder() \
            .setRowline(rowline) \
            .setColline(colline) \
            .setErrorType(errType) \
            .setMessage(msg) \
            .build()

        self.assertEqual(
            errMsg,
            "1:1 Unknown: Error message"
        )

if __name__ == "main":
    unittest.main()
