# -*- coding: utf-8 -*-
from annotation.models import Document, Label, AnnotationQueue, QueueElement
import annotation.classifier as clf

from random import sample
from operator import itemgetter

import logging
import pdb


def uncertainty_sampling(documents, trueLabels, saveScores=True):
    # the parameter documents should be straight forward. It's list of
    # documents to be sorted according to minimal margin sampling. The
    # parameter trueLabels is added for convenience as association between
    # documents and trueLabels usually is realised via the order in a
    # list.
    if documents and clf.predict(documents[0], saveScores):
        # predict the scores for all documents
        pred_scores = map(lambda d: clf.predict(d, saveScores), documents)
        # for every document sort the scores of all trueLabels
        sorted_scores = map(lambda score:
                            sorted(map(lambda val: val['normalized'],
                                       score.values()), reverse=True),
                            pred_scores)
        # calculate the margin between the two most likely trueLabels
        margin = lambda scores: scores[0]-scores[1] if len(scores) > 1 else scores[0]
        pred_margin = map(margin, sorted_scores)
        # associate the margins with their respective documents and sort
        # them
        doc_margin = sorted(zip(documents, trueLabels, pred_margin,
                                map(lambda s: clf.predict_label(None, s),
                                    pred_scores)),
                            key=itemgetter(2))
        # write results to db
        if saveScores:
            for dm in doc_margin:
                document, trueLabel, margin, predLabel = dm
                doc, created = Document.objects.get_or_create(pk=document.pk)
                doc.active_prediction = predLabel
                doc.margin = margin
                doc.save()
        # unzip the margins from the documents and return the documents
        return zip(*doc_margin)[:2]
    else:
        return [documents, trueLabels]


def selectDocument(user):
    queue = AnnotationQueue.objects.filter(user=user).first()
    document = Document(document='YOU HAVE NO MORE DOCUMENTS LEFT TO ANNOTATE. THANK YOU FOR YOUR PARTICIPATION!',
                                doc_id='',
                                preprocessed='',
                                trainInstance=True)
    proposal = None
    element = None

    if queue:
        elements = QueueElement.objects.filter(queue=queue).order_by('rank')
        if elements:
            element = elements.first()
            document = element.document
            proposal = element.proposalFlag
        #
    return document, proposal, element
