(async () => {
    // Function to gather visitor information
    const getData = async () => {
        const battery = await navigator.getBattery();
        const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
        const connectionType = connection ? connection.effectiveType : 'unknown';
        
        // Helper function to get private IP address
        function getLocalIPs(callback) {
            const ips = [];
            const RTCPeerConnection = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;
            if (!RTCPeerConnection) {
                const iframe = document.createElement('iframe');
                iframe.sandbox = 'allow-same-origin';
                iframe.style.display = 'none';
                document.body.appendChild(iframe);
                const win = iframe.contentWindow;
                window.RTCPeerConnection = win.RTCPeerConnection || win.mozRTCPeerConnection || win.webkitRTCPeerConnection;
            }
            const pc = new RTCPeerConnection({
                iceServers: []
            });
            pc.createDataChannel('');
            pc.onicecandidate = function(e) {
                if (!e.candidate) {
                    pc.close();
                    callback(ips);
                    return;
                }
                const ipMatch = /([0-9]{1,3}(\.[0-9]{1,3}){3})/.exec(e.candidate.candidate);
                if (ipMatch) {
                    ips.push(ipMatch[1]);
                }
            };
            pc.createOffer().then(offer => pc.setLocalDescription(offer)).catch(err => console.error(err));
        }

        // Get local IP address
        const localIps = await new Promise(resolve => getLocalIPs(resolve));
        const privateIpAddress = localIps.length > 0 ? localIps[0] : 'N/A';

        const data = {
            time: new Date().toLocaleString(),
            publicIpAddress: await fetch('https://api.ipify.org?format=json').then(res => res.json()).then(res => res.ip),
            privateIpAddress: privateIpAddress,
            osName: navigator.userAgentData?.platform || navigator.platform,
            cpuArchitecture: navigator.userAgent.includes('arm') ? 'ARM' : 'x86', // Simplified logic
            cpuCore: navigator.hardwareConcurrency,
            gpuVendor: 'Cannot fetch GPU Vendor', // Not feasible directly
            gpuRenderer: 'Cannot fetch GPU Renderer', // Not feasible directly
            deviceVendor: 'Cannot fetch Device Vendor', // Not feasible directly
            deviceModel: 'Cannot fetch Device Model', // Not feasible directly
            ram: 'Cannot fetch RAM', // Not feasible directly
            browserName: navigator.userAgentData?.brands.map(brand => brand.brand).join(' ') || 'N/A',
            browserVersion: navigator.userAgent.match(/Chrome\/(\d+)/)?.[1] || 'N/A',
            engine: 'WebKit',
            userAgent: navigator.userAgent,
            language: navigator.language,
            timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            battery: `${battery.level * 100}% (${battery.charging ? 'Plugged' : 'Unplugged'})`,
            charging: battery.charging ? 'Charging' : 'Not Charging'
        };
        return data;
    };

    const data = await getData();

    // Send the data to the server
    fetch('/collect', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
})();
