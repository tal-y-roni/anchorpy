from dataclasses import dataclass, field
from typing import List, Any, Tuple, Dict, Union, Optional

from solana.account import Account
from solana.publickey import PublicKey
from solana.rpc.types import TxOpts
from solana.transaction import AccountMeta, TransactionInstruction

from anchorpy.idl import IdlInstruction


class ArgsError(Exception):
    pass


# should be Dict[str, Union[PublicKey, Accounts]]
# but mypy doesn't support recursive types
Accounts = Dict[str, Union[PublicKey, Any]]


@dataclass
class Context:
    accounts: Accounts = field(default_factory=dict)
    remaining_accounts: List[AccountMeta] = field(default_factory=list)
    signers: List[Account] = field(default_factory=list)
    instructions: List[TransactionInstruction] = field(default_factory=list)
    options: Optional[TxOpts] = None


def split_args_and_context(
    idl_ix: IdlInstruction, args: List[Any]
) -> Tuple[List[Any], Context]:
    options = {}
    new_args = args
    if len(args) > len(idl_ix.args):
        if len(args) != len(idl_ix.args) + 1:
            raise ArgsError(f"Provided too many args to method={idl_ix.name}")
        new_args = args[:-1]
        options = args[-1]
    return new_args, Context(**options)