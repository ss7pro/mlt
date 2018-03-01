from mock import patch
import pytest

from mlt.utils.progress_bar import duration_progress


@patch('mlt.utils.progress_bar.progressbar')
def test_duration_progress_not_done(progressbar):
    """duration progress + not is_done once"""
    test_duration_progress_not_done.done = False

    def not_done():
        if test_duration_progress_not_done.done:
            return True
        test_duration_progress_not_done.done = True

    duration_progress('billy', 1, not_done)

    progressbar_obj = progressbar.ProgressBar.return_value.return_value
    assert progressbar_obj.next.call_count == 2
    assert progressbar_obj.update.call_count == 1


@patch('mlt.utils.progress_bar.progressbar')
def test_duration_progress_duration_done(progressbar):
    """duration progress + done immediately"""
    duration_progress('billy', 1, lambda: True)

    progressbar_obj = progressbar.ProgressBar.return_value.return_value
    assert progressbar_obj.next.call_count == 1
    assert progressbar_obj.update.call_count == 1


@patch('mlt.utils.progress_bar.progressbar')
def test_duration_progress_no_duration_not_done(progressbar):
    """no duration progress + not done + while not_is_done one iteration"""

    test_duration_progress_no_duration_not_done.done = 1

    def done():
        if test_duration_progress_no_duration_not_done.done | 3 == 3:
            test_duration_progress_no_duration_not_done.done += 1
            return False
        return True

    duration_progress('billy', None, done)

    progressbar_obj = progressbar.ProgressBar.return_value.return_value
    progressbar_obj.next.assert_not_called()
    progressbar_obj.update.call_count == 3


@patch('mlt.utils.progress_bar.progressbar')
def test_duration_progress_no_duration_done(progressbar):
    """no duration progress + done immediately"""
    duration_progress('billy', None, lambda: True)

    progressbar_obj = progressbar.ProgressBar.return_value.return_value
    progressbar_obj.next.assert_not_called()
    progressbar_obj.update.assert_not_called()
