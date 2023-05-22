import struct
from enum import Enum

from ..prof_common_func.constant import Constant


class MemoryEnum(Enum):
    PTR = 0
    TIME_NS = 1
    ALLOC_SIZE = 2
    TOTAL_ALLOCATED = 3
    TOTAL_RESERVED = 4
    DEVICE_TYPE = 5
    DEVICE_INDEX = 6
    THREAD_ID = 7
    PROCESS_ID = 8


class MemoryUseBean:
    CONSTANT_STRUCT = "<5qbB2Q"

    def __init__(self, data: dict):
        self._origin_data = data
        self._constant_data = struct.unpack(self.CONSTANT_STRUCT, data.get(Constant.CONSTANT_BYTES))

    @property
    def ptr(self) -> int:
        return int(self._constant_data[MemoryEnum.PTR.value])

    @property
    def time_us(self) -> float:
        return int(self._constant_data[MemoryEnum.TIME_NS.value]) / 1000.0

    @property
    def alloc_size(self) -> int:
        return int(self._constant_data[MemoryEnum.ALLOC_SIZE.value])

    @property
    def total_allocated(self) -> int:
        return int(self._constant_data[MemoryEnum.TOTAL_ALLOCATED.value])

    @property
    def total_reserved(self) -> int:
        return int(self._constant_data[MemoryEnum.TOTAL_RESERVED.value])

    @property
    def device_type(self) -> int:
        return int(self._constant_data[MemoryEnum.DEVICE_TYPE.value])

    @property
    def device_index(self) -> int:
        return int(self._constant_data[MemoryEnum.DEVICE_INDEX.value])

    @property
    def tid(self) -> int:
        return int(self._constant_data[MemoryEnum.THREAD_ID.value])

    @property
    def pid(self) -> int:
        return int(self._constant_data[MemoryEnum.PROCESS_ID.value])