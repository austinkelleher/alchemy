# -*- coding: utf-8 -*-
import numpy as np
import string


class ART(object):

  """Associative retrieval task (ART + mART)"""

  def __init__(self, chars=list(string.ascii_lowercase)):
    self._chars = chars
    self._chars_size = len(self._chars) - 1
    self._alphabet = self._chars + [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '?']
    self._alphabet_size = len(self._alphabet) - 1
    self._encoder = np.eye(self._alphabet_size + 1)

  def ordinal_to_alpha(self, sequence):
    conversion = ""
    for item in sequence:
      conversion += str(self._alphabet[int(item)])
    return conversion

  def create_example(self, k=8, use_modified=False):
    q, r = divmod(k, 2)
    assert r == 0 and k > 1 and k < self._alphabet_size, \
        "k must be even, > 1, and < {}".format(self._alphabet_size)

    letters = np.random.choice(range(0, self._chars_size), q, replace=False)
    numbers = np.random.choice(
        range(self._chars_size + 1, self._alphabet_size), q, replace=True)
    if use_modified:
      x = np.concatenate((letters, numbers))
    else:
      x = np.stack((letters, numbers)).T.ravel()

    x = np.append(x, [self._alphabet_size, self._alphabet_size])
    index = np.random.choice(range(0, q), 1, replace=False)
    x = np.append(x, [letters[index]]).astype('int')
    y = numbers[index]
    return self._encoder[x], self._encoder[y][0]

  def create_dataset(self, num_samples, k=8, use_modified=False):
    size = len(self._encoder)
    X = np.empty([num_samples, k, size], dtype=np.int32)
    y = np.empty([num_samples, size], dtype=np.int32)
    for i in range(num_samples):
      x[i], y[i] = self.create_example(k=k, use_modified=use_modified)
    return x, y