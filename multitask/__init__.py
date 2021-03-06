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
    fun: Callable, iterable: Iterable, n_cores: int = cpu_count(),
    chunksize: int = 1, *args, **kwargs
) -> list:
    """
    tqdmを使ってimap_unorderedを呼び出す。

    Args:
        fun (Callable):
            呼び出す関数。
        iterable (Iterable):
            引数。
        n_cores (int, optional):
            計算に使うコア数。デフォルトはCPU数。
        chunksize (int, optional):
            並列計算の分割サイズ。デフォルトは1。
        args, kwargs:
            tqdmに渡されるパラメーター。

    Returns:
        list: 計算結果。
    """
    if n_cores == 1:
        return [fun(i) for i in  tqdm(iterable, *args, **kwargs)]
    prog_bar = tqdm(total=len(iterable), *args, **kwargs)
    pool = Pool(n_cores)
    result = list()
    try:
        for i in pool.imap_unordered(fun, iterable, chunksize=chunksize):
            result.append(i)
            prog_bar.update(1)
    finally:
        pool.close()
        pool.join()
        prog_bar.close()
    return result


__all__ = ["imap_unordered_with_tqdm"]
