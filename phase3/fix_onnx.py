import onnx
import sys

def fix_onnx(model_path):
    print(f"Fixing {model_path}...")
    model = onnx.load(model_path)

    # Get names of inputs and outputs
    io_names = set([i.name for i in model.graph.input] + [o.name for o in model.graph.output])

    # Remove any value_info that has the same name as an input or output
    new_value_info = []
    for vi in model.graph.value_info:
        if vi.name not in io_names:
            new_value_info.append(vi)
        else:
            print(f"Removing {vi.name} from value_info")

    # Clear the old value_info and add the new ones
    del model.graph.value_info[:]
    model.graph.value_info.extend(new_value_info)

    # Save the fixed model
    onnx.save(model, model_path)
    print("Fix complete.")

if __name__ == "__main__":
    fix_onnx("phase3/custom_model/best.onnx")
