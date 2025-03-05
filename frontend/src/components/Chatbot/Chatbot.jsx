import React from "react";
import { useEffect, useState } from "react";
import "./Chatbot.css";
import send from "../../img/send.svg";
import header from "../../img/header.png";

// import { Link } from 'react-router-dom'

const Chatbot = () => {
    const [query, setQuery] = useState("");
    // this is the chat interface data display, we can delete the below list such that we dont have any thing
    const [data, setdata] = useState([
        {
			content: "Hello",
			isChatbot: false
		},
		{
			content: "How can I help you?",
			isChatbot: true
		}
    ]);
    function changeValue(e) {
        setQuery(e.target.value);
    }

    // function to send the data to the server below is the local host address
    async function sendData() {
        const todo = query;
        console.log(query, "aa");
		setQuery("");
        const response = await fetch("http://127.0.0.1:5000/add_todo", {
            method: "POST", // post is to send the data and fetch is to get the response
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({question: todo}),
        });
        // to send the response the SetQuery which show the chat in the display
        if (response.ok) {
            response.json().then((response) => {
                console.log(data);
				const question = {
					content: query,
					isChatbot: false
				};
                const answer = {
					content: response.message,
					isChatbot: true
				};
                setdata(messages => [...messages, question, answer]);
            });
        }
    }

    // useEffect(()=>{
    //   sendData()
    // },[data])

    // function fetchData(){
    //     fetch("http://127.0.0.1:5000/add_todo").then((res) =>{
    //         console.log(res)
    //         res.json().then((data) => {
    //           console.log(data)
    //             // Setting a data from api
    //             // setdata({
    //             //     name: data.Name,
    //             //     age: data.Age,
    //             //     date: data.Date,
    //             //     programming: data.programming,
    //             // });
    //         })
    //       }
    //     );
    // }

    // const a = [
    //   {
    //     "question": "What is this",
    //     "answer" : "This this the answer"
    //   },
    //   {
    //     "question": "what is the second question",
    //     "answer": "Ths is the second answer"
    //   },
    //   {
    //     "question": "what is the second question",
    //     "answer": "Ths is the second answer"
    //   },
    //   {
    //     "question": "what is the second question",
    //     "answer": "Ths is the second answer"
    //   },
    //   {
    //     "question": "what is the second question",
    //     "answer": "Ths is the second answer"
    //   }
    // ]
    // console.log(a.map(()=>{

    // }))
    // const [answer,S]
    return (
        <div className="App">
            <img id="one" src={header} alt="" />
            <div className="sidebar">
                <div className="upperSide">
                    <div className="upperSideTop">
                        <span className="brand">Chatbot</span>
                        <button className="addBtn">New Chat</button>
                        <div className="upperSideBottom">
                            <button className="query">
                                <img src={send} alt="" />
                                What is the right season to grow apple?
                            </button>
                            <button className="query">
                                <img src={send} alt="" />
                                In which place carrot grows healthy?
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <div className="main">
				<h2>GreenThumb Chatbot</h2>
                <div className="chats">
                    {data.map((e, ind) => {
                        return (
							<div className="chat-row" key={ind}>
								<div className={e.isChatbot ? "chat bot" :"chat"}>
									<p>{e.content}</p>
								</div>
							</div>
                        );
                    })}
                </div>
                <div className="chatFooter">
                    <div className="inp">
                        <input
                            type="text"
                            placeholder="Send a message"
                            value={query}
                            onChange={changeValue}
                        />
                        <button className="send">
                            <img src={send} onClick={sendData} alt="" />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Chatbot;
