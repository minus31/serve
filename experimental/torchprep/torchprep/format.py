import yaml
import torch
from typing import Dict, List, Union


dtype_map = {
    # randn
    "float32" : torch.float32,
    "float"     : torch.float,
    "float64" : torch.float64,
    "half"    : torch.half,
    "float16" : torch.float16,
    "bfloat16" : torch.bfloat16,
    "complex64" : torch.complex64,
    "complex128" : torch.complex128,
    "cdouble"    : torch.cdouble,

    # randint
    "uint8" : torch.uint8, 
    "int8" : torch.int8,
    "int16" : torch.int16,
    "short" : torch.short,
    "int32" : torch.int32,
    "int"   : torch.int ,
    "int64" : torch.int64,
    "long" : torch.long,
    "bool" : torch.bool,
    "quint8" : torch.qint8,
    "qint8" : torch.qint8,
    # "qfint32" : torch.qfint32,
    # "qint4x2" : torch.quint4x2,
}

device_map = {
    "CPU" : torch.device("cpu"),
    "cpu" : torch.device("cpu"),
    "gpu" : torch.device("cuda"),
    "GPU" : torch.device("cuda"),
    "cuda" : torch.device("cuda")
}

def parse_input_format(filename : str = "example.yaml") -> Dict[str, Union[int, List[int]]]: 
    with open(filename, 'r') as f:
        try:
            parsed_yaml=yaml.safe_load(f)
            print(parsed_yaml)
        except yaml.YAMLError as exc:
            print(exc)

def materialize_tensors(yaml_dict) -> List[torch.Tensor]:
    for key, value in yaml_dict.items():
        tensor_list = []
        # If a new input is found
        if key.startswith("input"):
            input_params = yaml_dict[value]

            for input_key, input_value in input_params:
                if input_key == "shape":
                    shape = input_value     
                elif input_key == "dtype":
                    dtype = input_value
                elif input_key == "device":
                    device = input_value
                elif input_key == "mode":
                    mode = input_value
                elif input_key == "high":
                    high = input_value

            # Mode is optional, users can just hard code a batch size
            for idx, dimension in enumerate(shape):
                if dimension == -1:
                    if mode == "latency":
                        shape[idx] = 1
                    elif mode == "throughput":
                        shape[idx] = 1024

            if dtype in ["float32", "float", "float64", "half", "float16", "bfloat16", "complex64", "complex128", "cdouble"]:
                x = torch.randn(*shape, dtype=dtype_map[dtype], device=device_map[device]) * high

            elif dtype in ["uint8", "int8", "int16", "short", "int32", "int", "int64", "long", "bool", "quint8", "qint8"]:
                torch.randint(low=0, high=high, size = tuple(shape), dtype=dtype_map[dtype])
            else:
                print("dtype {dtype} is no supported")
                return

            tensor_list.append(x)

        return tensor_list