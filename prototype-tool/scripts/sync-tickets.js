const fs = require('fs');
const path = require('path');

const TICKETS_DIR = path.join(__dirname, '../decision-tickets');
const OUTPUT_FILE = path.join(__dirname, '../frontend/lib/tickets-data.json');

function mapStatus(status) {
    if (!status) return 'proposed';
    const s = status.toLowerCase();
    if (s === 'decided') return 'accepted';
    if (s === 'open') return 'proposed';
    return s;
}

function syncTickets() {
    if (!fs.existsSync(TICKETS_DIR)) {
        console.error(`Directory not found: ${TICKETS_DIR}`);
        process.exit(1);
    }

    const files = fs.readdirSync(TICKETS_DIR).filter(f => f.endsWith('.json'));
    const tickets = [];

    files.forEach(file => {
        const filePath = path.join(TICKETS_DIR, file);
        const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));

        // Generate ID following DEC-I/P/D####
        let prefix = 'DEC-';
        if (file.startsWith('issue')) prefix += 'I';
        else if (file.startsWith('pr')) prefix += 'P';
        else if (file.startsWith('discussion')) prefix += 'D';
        else prefix += 'X';

        const idMatch = file.match(/\d+/);
        const id = idMatch ? `${prefix}${idMatch[0]}` : `${prefix}${Math.random().toString(36).substr(2, 5)}`;

        const sharedArguments = (data.Argument || []).map((arg, idx) => ({
            id: `arg-${id}-${idx}`,
            content: arg.argument || '',
            type: 'neutral',
            author: arg.author || '',
            createdAt: arg.timestamp || '',
            timestamp: arg.timestamp || '',
            argument: arg.argument || ''
        }));

        const ticket = {
            id: id,
            title: data.Issue || '',
            decision: data.Decision || '',
            rationale: data.Rationale || '',
            status: mapStatus(data.Status),
            description: data.Description || '',
            timestamp: data['Time stamp'] || '',
            cost: data.Cost || '',
            risk: data.Risk || '',
            author: data.Author || '',
            arguments: sharedArguments,
            
            // Dashboard compatibility mappings
            bucket: data['Mapped Stage'] || 'Miscellaneous',
            owner: {
                id: `agent-${data.Author || 'unknown'}`,
                name: data.Author || ''
            },
            createdAt: data['Time stamp']?.split(',')[0]?.split('(')[0]?.trim() || '',
            updatedAt: '',
            tags: [], 
            currentVersionIndex: 0,
            versions: [
                {
                    versionId: 'v1',
                    decision: data.Decision || '',
                    rationale: data.Rationale || '',
                    context: data.Description || '',
                    cost: data.Cost || '',
                    risk: data.Risk || '',
                    arguments: sharedArguments,
                    artifacts: [],
                    parentVersionId: null,
                    nodes: [],
                    edges: []
                }
            ]
        };

        tickets.push(ticket);
    });

    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(tickets, null, 2));
    console.log(`Successfully synced ${tickets.length} tickets to ${OUTPUT_FILE}`);
}

syncTickets();
