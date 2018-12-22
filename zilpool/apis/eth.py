# -*- coding: utf-8 -*-
# Zilliqa Mining Pool
# Copyright @ 2018-2019 Gully Chen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Tuple
from jsonrpcserver import method

from zilpool.database import pow


def init_apis(config):
    no_work = ("", "", "")

    @method
    async def eth_getWork() -> [List, Tuple]:
        min_fee = config.mining["min_fee"]
        max_dispatch = config.mining["max_dispatch"]
        work = pow.PowWork.get_new_works(count=1, min_fee=min_fee,
                                         max_dispatch=max_dispatch)
        if not work:
            return no_work

        if work.increase_dispatched():
            return work.header, work.seed, work.boundary
        return no_work

    @method
    async def eth_submitWork(nonce: str, header: str, boundary: str,
                             mix_digest: str, miner_wallet: str) -> bool:
        assert (len(nonce) == 18 and
                len(header) == 66 and
                len(boundary) == 66 and
                len(mix_digest) == 66 and
                len(miner_wallet) == 42)

        work = pow.PowWork.find_work_by_header_boundary(header=header, boundary=boundary)
        if not work:
            return False

        # verify result

        return True

    @method
    async def eth_submitHashrate(hashrate: str, miner_id: str) -> bool:
        assert (len(hashrate) == 66 and
                len(miner_id) == 66)
        return True