
def run_cell(input_file):
    exec(input_file, globals())

def check_for_gpu():
    try:
        exec('''
import torch
torch.tensor([1.,]).cuda()
        ''', globals())
        return True
    except:
        return False