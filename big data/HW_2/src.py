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

    def is_duplicate(self, obj1, obj2):
        name1, name2 = obj1['Название'].lower().replace(',', '').replace('-', ' '), \
                       obj2['Название'].lower().replace(',', '').replace('-', ' ')
        score_name = edit_distance(name1, name2)[0] < 1
        kernel1, kernel2 = obj1['Ядро'].lower().replace('-', ''), obj2['Ядро'].lower().replace('-', '')
        score_kernel = edit_distance(kernel1, kernel2)[0] < 2
        kernels_num1, kernels_num2 = int(obj1['Количество ядер']), int(obj2['Количество ядер'])
        score_kernels_num = kernels_num1 == kernels_num2
        return score_name and score_kernel and score_kernels_num

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
                    sys.stdout.write(json.dumps(obj_i, indent=4, ensure_ascii=False).encode())
                    sys.stdout.write('\n'.encode())
                    sys.stdout.write(json.dumps(obj_j, indent=4, ensure_ascii=False).encode())
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
