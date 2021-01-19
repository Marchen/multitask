"""
並列計算支援モジュール。
"""

from multiprocessing import Pool, cpu_count
import sys
from typing import Callable, Iterable, Union

if 'ipykernel' in sys.modules:
    from tqdm import tqdm_notebook as tqdm
else:
    from tqdm import tqdm

# -----------------------------------------------------------------------------
def imap_unordered_with_tqdm(
    fun: Callable, args: Iterable, n_cores: int = cpu_count(),
    desc: Union[str, None]=None
) -> list:
    """
    tqdmを使ってimap_unorderedを呼び出す。

    Args:
        fun (Callable):
            呼び出す関数。
        args (Iterable):
            引数。
        n_cores (int, optional):
            計算に使うコア数。デフォルトはN_CORES。

    Returns:
        list: 計算結果。
    """
    prog_bar = tqdm(total=len(args), desc=desc)
    pool = Pool(n_cores)
    result = list()
    try:
        for i in pool.imap_unordered(fun, args):
            result.append(i)
            prog_bar.update(1)
    finally:
        pool.close()
        pool.join()
        prog_bar.close()
    return result


__all__ = ["imap_unordered_with_tqdm"]
