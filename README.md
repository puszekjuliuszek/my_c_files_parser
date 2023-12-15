# my_c_files_parser
## how to use
run:
```angular2html
git clone https://github.com/puszekjuliuszek/my_c_files_parser
```

give path to your c file and thats all

## the output of parser
.json file of structure:
```angular2html
{
'array_info': [('A', [4096, 4096])], 
'loop_bounds': [('i', 0, 4096, 1), ('j', 0, 8, 1), ('k', 0, 4096, 1)], 
'data_deps': [[['A', 'k', 'i'], ['A', 'k', 'i'], ['A', 'k', 'i'], 90]]
}
```
## license