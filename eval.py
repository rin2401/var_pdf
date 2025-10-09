import sys

sys.path.append("../READoc/src/evaluation")

from suite_e2e import file_evaluate


def eval_md(md_label, md_text):
    res = file_evaluate(md_label, md_text)

    result_dict = {
        "text_concat": res["plain"].metric_dict["metrics"]["edit_dist_sim"],
        "text_vocab": res["plain"].metric_dict["metrics"]["f_measure"],
        "head_concat": res["head"].metric_dict["concated"]["edit_dist_sim"],
        "head_tree": res["head"].metric_dict["logical"]["teds"],
        "order_block": float(res["order"].metric_dict["segment"]["kendall_tau"]),
        "order_word": float(res["order"].metric_dict["word"]["kendall_tau"]),
    }

    if res["math"].metric_dict["inline_concated"]:
        result_dict["formula_inline"] = res["math"].metric_dict["inline_concated"][
            "edit_dist_sim"
        ]
    if res["math"].metric_dict["outline_concated"]:
        result_dict["formula_outline"] = res["math"].metric_dict["outline_concated"][
            "teds_min"
        ]

    if res["table"].metric_dict["concated"]:
        result_dict["table_concat"] = res["table"].metric_dict["concated"][
            "edit_dist_sim"
        ]
    if res["table"].metric_dict["mapped"]:
        result_dict["table_mapped"] = res["table"].metric_dict["mapped"]["teds_min"]

    res = {"score": sum(result_dict.values()) / len(result_dict), "detail": result_dict}

    return res


def eval(label_path, pred_path):
    with open(label_path, "r") as f:
        md_label = f.read()
    with open(pred_path, "r") as f:
        md_text = f.read()
    return eval_md(md_label, md_text)


if __name__ == "__main__":
    idx = "Public061"
    res = eval(
        f"../submit/public_label/{idx}/main.md",
        f"../submit/pymuf4llm_output/{idx}/main.md",
    )

    print(res)
