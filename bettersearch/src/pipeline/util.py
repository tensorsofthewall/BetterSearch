import os
import shutil
from collections import defaultdict
import nncf
import openvino as ov
from optimum.intel.openvino import OVModelForCausalLM
from optimum.intel import OVQuantizer

def download_and_save_model(model_id, save_dir, fp_gen = "INT4"):
    _, model_name = model_id.split("/")
    ov_model = OVModelForCausalLM.from_pretrained(model_id=model_id, export=True, compile=False, load_in_8bit=False)
    
    # Save in FP32
    if fp_gen == "FP32":
        ov_model.save_pretrained(f"{save_dir}/{model_name}/FP32")
    # Save in FP16
    if fp_gen == "FP16":
        ov_model.half()
        ov_model.save_pretrained(f"{save_dir}/{model_name}/FP16")
    # Save in INT8
    elif fp_gen == "INT8":
        ov_quantizer = OVQuantizer.from_pretrained(ov_model)
        ov_quantizer.quantize(save_directory=f"{save_dir}/{model_name}/INT8", weights_only=True)
    # Save in INT4
    elif fp_gen == "INT4":
        ov_model.save_pretrained(f"{save_dir}/{model_name}/FP16")
        compressed_model = nncf.compress_weights(
            ov_model.half()._original_model,
            mode=nncf.CompressWeightsMode.INT4_ASYM,
            group_size=128,
            ratio=0.8
        )
        ov.save_model(compressed_model, f"{save_dir}/{model_name}/INT4/openvino_model.xml")
        shutil.copy(f"{save_dir}/{model_name}/FP16/config.json", f"{save_dir}/{model_name}/INT4/config.json")
        shutil.rmtree(f"{save_dir}/{model_name}")
        


def get_available_models(save_dir):
    available_models = defaultdict(list)
    for model_name in os.listdir(save_dir):
        model_dir = os.path.join(save_dir, model_name)
        if os.path.isdir(model_dir):
            for precision in os.listdir(model_dir):
                precision_path = os.path.join(model_dir, precision)
                if os.path.isdir(precision_path):
                    available_models[precision].append(model_name)
    
    return available_models