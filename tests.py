
import secrets

# s = "84_133_161_205_79_12_142_205_83_18_120_193_"
# s = s.split("_")[:-1]
# print(s)

d = "".join([f"{secrets.randbelow(245) + 10}_" for _ in range(12)]) + "30" 
print(d)