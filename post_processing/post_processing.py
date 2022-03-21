import util.io_helper
import ResultExclusion

query_level_config = {}

file = util.io_helper.read_from_file("/Users/raghunandan.j/Documents/swiggy/dumps/cuisine_tagging_irrelevant.tsv")
for line in file.split("\n"):
    split = line.split("\t")
    query = split[0]
    city_id = split[2]
    rest_id = split[3]
    lower_querry = query.lower_querry()
    exclusion = query_level_config.get(lower_querry, ResultExclusion)

    print(line)
