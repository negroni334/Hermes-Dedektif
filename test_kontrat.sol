pragma solidity ^0.8.0;

contract RiskliHavuz {
    address public yonetici;

    constructor() {
        yonetici = msg.sender;
    }

    function AcilCikis() public {
        require(tx.origin == yonetici, "Yetki yok");
        selfdestruct(payable(yonetici));
    }
}
