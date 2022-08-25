import random
import numpy as np
import json


def evaluate(test_annotation_file, user_submission_file, phase_codename, **kwargs):
    print("Starting Evaluation.....")
    """
    Evaluates the submission for a particular challenge phase and returns score
    Arguments:

        `test_annotations_file`: Path to test_annotation_file on the server
        `user_submission_file`: Path to file submitted by the user
        `phase_codename`: Phase to which submission is made

        `**kwargs`: keyword arguments that contains additional submission
        metadata that challenge hosts can use to send slack notification.
        You can access the submission metadata
        with kwargs['submission_metadata']

        Example: A sample submission metadata can be accessed like this:
        >>> print(kwargs['submission_metadata'])
        {
            'status': u'running',
            'when_made_public': None,
            'participant_team': 5,
            'input_file': 'https://abc.xyz/path/to/submission/file.json',
            'execution_time': u'123',
            'publication_url': u'ABC',
            'challenge_phase': 1,
            'created_by': u'ABC',
            'stdout_file': 'https://abc.xyz/path/to/stdout/file.json',
            'method_name': u'Test',
            'stderr_file': 'https://abc.xyz/path/to/stderr/file.json',
            'participant_team_name': u'Test Team',
            'project_url': u'http://foo.bar',
            'method_description': u'ABC',
            'is_public': False,
            'submission_result_file': 'https://abc.xyz/path/result/file.json',
            'id': 123,
            'submitted_at': u'2017-03-20T19:22:03.880652Z'
        }
    """

    print(kwargs["submission_metadata"])

    with open(test_annotation_file, "r") as f:
        GT = json.load(f)

    with open(user_submission_file, "r") as f:
        result = json.load(f)

    scores = {}

    for key, score in result.items():
        trial_name = GT[key][0]
        test_class = GT[key][1]

        if trial_name not in scores:
            scores[trial_name] = {}
        scores[trial_name][test_class] = score

    acc_1 = []
    acc_2 = []
    acc_3 = []
    acc_4 = []
    acc_all = []

    for trial_name, ratings in scores.items():
        if abs(ratings["expected"] - ratings["surprising"]) < 1e-6:
            correct = 0.5
        else:
            if ratings["expected"] < ratings["surprising"]:
                correct = 1
            else:
                correct = 0
        if "scenario_1" in trial_name:
            acc_1.append(correct)
        if "scenario_2" in trial_name:
            acc_2.append(correct)
        if "scenario_3" in trial_name:
            acc_3.append(correct)
        if "scenario_4" in trial_name:
            acc_4.append(correct)
        acc_all.append(correct)

    output = {}
    if phase_codename == "test":
        print("Evaluating for Test Phase")
        output["result"] = [
            {
                "test_split": {
                    "Scneario 1": np.mean(acc_1),
                    "Scneario 2": np.mean(acc_2),
                    "Scneario 3": np.mean(acc_3),
                    "Scneario 4": np.mean(acc_4),
                    "All": np.mean(acc_all),
                }
            },
        ]
        # To display the results in the result file
        output["submission_result"] = output["result"][0]
        print("Completed evaluation for Test Phase")
    return output
