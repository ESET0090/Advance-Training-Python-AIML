
interface BaseAPIResponse {
    message: string;
    traceId: string;
}

interface LCData {
    name : string;
    uv : number;
    pv : number;
    amt : number;
}

interface DashboardApiResponse extends BaseAPIResponse {
    data: LCData;
}

