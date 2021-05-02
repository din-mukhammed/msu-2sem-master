import json

from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import JSONProtocol

from helper import *


class DataFusion(MRJob):

    def mapper_raw(self, input_path, input_uri):
        global is_filled_dns
        global is_filled_citilink
        IS_CITILINK_FILE = CITILINK_FILENAME in input_path
        IS_DNS_FILE = DNS_FILENAME in input_path
        with open(input_path, 'r') as file:
            data = json.load(file)
        for obj in data:
            if IS_CITILINK_FILE and not is_filled_citilink:
                fields.update(obj.keys())
                is_filled_citilink = True
            if IS_DNS_FILE and not is_filled_dns:
                fields.update(obj.keys())
                is_filled_dns = True
            yield obj['duplicate_id'], (obj, DNS_FILENAME if IS_DNS_FILE else CITILINK_FILENAME)

    def reducer(self, dup_id, objs):
        objs = [*objs]
        obj1, src1, obj2, src2 = objs[0][0], objs[0][1], objs[1][0], objs[1][1]

        for field in fields:
            val1, val2 = obj1.get(field), obj2.get(field)
            if val1 is None or val2 is None:
                obj1[field] = resolve(
                    vals=[val1, src1, val2, src2], resolve_fun=choose_not_none)
            else:
                obj1[field] = resolve(
                    vals=[val1, src1, val2, src2], resolve_fun=resolver_funcs[field])
        del obj1['duplicate_id']
        sys.stdout.write(json.dumps(
            obj1, indent=4, ensure_ascii=False).encode())
        sys.stdout.write(',\n'.encode())

    def steps(self):
        return [
            MRStep(
                mapper_raw=self.mapper_raw,
                reducer=self.reducer
            )
        ]


if __name__ == '__main__':
    DataFusion.run()
