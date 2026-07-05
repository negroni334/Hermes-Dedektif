pragma solidity ^0.8.0;

contract RiskliHavuz {
    address public yonetici;

    constructor() {
        yonetici = msg.sender;
    }

    function AcilCikis() public {
        // Kritik Hata 1
        require(tx.origin == yonetici, "Yetki yok");
        
        // Kritik Hata 2
        selfdestruct(payable(yonetici));
    }
}
