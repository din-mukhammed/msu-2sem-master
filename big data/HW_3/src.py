import json
import codecs
import sys

from edit_distance import edit_distance

from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import JSONProtocol
seen = [-1 for i in range(10)]


class FindDups(MRJob):

    def mapper_raw(self, input_path, input_uri):
        with codecs.open(input_path, 'r', encoding='cp1251') as file:
            data = json.load(file)
        for obj in data:
            name = obj['Название']
            name = name.replace('-', ' ')
            name = ' '.join(name.lower().split(',')[0].split()[:2])
            yield hash('-'.join([name])), obj

    def reducer(self, _, vals):
        vals = list(vals)
        for i, obj_i in enumerate(vals):
            for j in range(i + 1, len(vals)):
                obj_j = vals[j]
                if self.is_duplicate(obj_i, obj_j):
                    idx = seen.index(-1)
                    seen[idx] = 1
                    obj_i['duplicate_id'], obj_j['duplicate_id'] = idx, idx
                    yield idx, (obj_i['Название'], obj_j['Название'])
                    sys.stdout.write(json.dumps(
                        obj_i, indent=4, ensure_ascii=False).encode())
                    sys.stdout.write('\n'.encode())
                    sys.stdout.write(json.dumps(
                        obj_j, indent=4, ensure_ascii=False).encode())
                    sys.stdout.write('\n'.encode())

    def steps(self):
        return [
            MRStep(
                mapper_raw=self.mapper_raw,
                reducer=self.reducer
            )
        ]


if __name__ == '__main__':
    FindDups.run()
