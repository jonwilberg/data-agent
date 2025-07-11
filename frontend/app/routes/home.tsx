import type { Route } from "./+types/home";
import { Welcome } from "../welcome/welcome";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Census Data Explorer" },
    { name: "description", content: "Ask natural language questions about US census data and get instant insights" },
  ];
}

export default function Home() {
  return <Welcome />;
}
