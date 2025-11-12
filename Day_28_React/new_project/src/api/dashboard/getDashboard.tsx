import { use, useState } from "react";


export const getDashboard = () => {

    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState();
    const [data, setData] = useState<LCData[]>([]);

    useEffect(() => {
        const getData = async () => {
            axios.get<DashboardAPiResponse>('http://localhost:9000');
        }

        getData();
}, []);

