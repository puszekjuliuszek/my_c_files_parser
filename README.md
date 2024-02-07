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
'array_info': ('array_name', [height, width]),
'loop_bounds': ('iterator', start, end, jump)
'data_deps':   [operation, [[operation, [arguments]] ] ]
```

Example for test.c
```angular2html
{
'array_info': [('A', [4096, 4096])], 

'loop_bounds': [('i', 0, 4096, 1), ('j', 0, 8, 1), ('k', 0, 4096, 1)], 

'data_deps': [['Assignment', ['ArrayRef', ['ArrayRef', 'A', 'k'], 'i'], ['BinaryOp', ['BinaryOp', ['ArrayRef', ['ArrayRef', 'A', 'k'], 'i'], ['ArrayRef', ['ArrayRef', 'A', 'k'], ['BinaryOp', 'i', 5]]], 90]]]
}
```
## license