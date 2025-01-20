import { Link } from "react-router-dom";
import '../styles/NotFound.css'

export default function NotFound() {
    return (
        <div className="error">
            <h1><b>Page not found!</b></h1>
            <p>Go to the <Link to="/">Homepage</Link>.</p>
        </div>
    )
}