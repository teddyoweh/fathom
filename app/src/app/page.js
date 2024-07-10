"use client"
import Image from "next/image";
import "./style.scss";
import axios from "axios";
import { useState } from "react";
export default function Home() {
  const [keyword, setKeyword] = useState("");
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const headers =   {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept':"*/*",
    'Access-Control-Allow-Origin': '*',
   }
   function getLinkedInUsername(url) {
    const parts = url.split('/');
    return parts[parts.length - 1] || parts[parts.length - 2];
}
   const [contacts, setContacts] = useState({});
   async function fetchContact(username) {
    setLoading(true);
 await axios.post(
      "http://127.0.0.1:5000/profile",
      {
        username: getLinkedInUsername(username),
      },
      // {
      //   headers: headers,
      // }
    ).then((response) => {
     // set contact key pair, username: response.data

     console.log(response.data);
     setContacts((prevContacts) => ({
      ...prevContacts,
      [getLinkedInUsername(item.profile)]: response.data,

    }));
    console.log(contacts);
      setLoading(false);
      
    }
    ).catch((error) => {
      console.log(error);
    });
 
  }
  async function fetchData() {
    setLoading(true);
 await axios.post(
      "http://127.0.0.1:5000/search",
      {
        keyword: keyword,
      },
      // {
      //   headers: headers,
      // }
    ).then((response) => {
      setData(response.data);
  
      setLoading(false);
    }
    ).catch((error) => {
      console.log(error);
    });
 
  }
  return (
    <div className="app">
      <div className="hero">
        <div className="hero-text">
          <label>
            Find the <span>best leads.</span> Seal the best <span>deals.</span>
          </label>
        </div>
        <div className="input-box">
          
          <input 
          disabled={loading}
          onChange={
            (e) => {
              setKeyword(e.target.value);
            }
          } onKeyPress={
            (e) => {
              if (e.key === "Enter") {
                fetchData();
              }
            }
          } type="text" placeholder="Search for leads..." />
          {loading==true &&<span className="loader"></span>}
        </div>
      </div>
      <div className="data">
        {
 
          data &&

          <div className="data-list">
            <small>
              {data.length} results found for {keyword}
            </small>
            {
              data.map((item, index) => {
                return (
                  <div className="dx">

       
                  <div key={index} className="data-item slide-up">
                    <div className="data-item-image">
                      <img 
                      onClick={() => {
                        fetchContact(item.profile);

                      }}
                      src="https://media.idownloadblog.com/wp-content/uploads/2017/03/Twitter-new-2017-avatar-001.png" alt="" />
                    </div>
                    <div className="data-item-text">
                    <a href={item.profile} target="_blank">{item.Name}</a>
                      <label className="loc">{item.location}</label>
              
                    </div>
                  </div>
                  {
                    Object.keys(contacts).includes(getLinkedInUsername(item.profile)) &&
                    <div className="contact-info">
                      {JSON.stringify(contacts[getLinkedInUsername(item.profile)])}
                    </div>   
                  }
     

                 
                  </div>
                );
              })
            }
        
      </div>
}
</div>
    </div>
  );
}
