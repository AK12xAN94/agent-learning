from p5Agent.utils.config_handler import prompts_config
from p5Agent.utils.path_tool import get_abs_path
from p5Agent.utils.logger_handler import logger

def load_system_prompts() -> dict[str, str]:
    try:
        system_prompt_path = get_abs_path(prompts_config["main_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_system_prompts]加载系统提示词失败: {e}")
        raise e

    try:
        return open(system_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_system_prompts]加载系统提示词失败: {e}")
        raise e

def load_rag_prompts() -> dict[str, str]:
    try:
        rag_prompt_path = get_abs_path(prompts_config["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_rag_prompts]在yaml配置中未找到rag_summarize_prompt_path配置项: {e}")
        raise e

    try:
        return open(rag_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_rag_prompts]加载rag提示词失败: {e}")
        raise e

def load_report_prompts() -> dict[str, str]:
    try:
        report_prompt_path = get_abs_path(prompts_config["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_report_prompts]在yaml配置中未找到report_prompt_path配置项: {e}")
        raise e

    try:
        return open(report_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_report_prompts]加载report提示词失败: {e}")
        raise e