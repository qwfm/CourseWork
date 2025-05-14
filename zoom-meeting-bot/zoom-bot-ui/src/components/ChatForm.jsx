import React, { useState, useEffect } from 'react';

export default function ChatForm() {
  const [to, setTo] = useState('');
  const [message, setMessage] = useState('');
  const [channels, setChannels] = useState([]);

  useEffect(() => {
    const loadChannels = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/channels`);
        const data = await response.json();
        setChannels(data.channels || []);
      } catch (error) {
        console.error('Помилка завантаження каналів:', error);
      }
    };
    loadChannels();
  }, []);

  const sendChat = async e => {
    e.preventDefault();
    if (!to || !message) {
      alert('Заповніть всі поля');
      return;
    }
    
    try {
      const resp = await fetch(`${process.env.REACT_APP_API_BASE_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ to, message })
      });
      const data = await resp.json();
      alert(`Повідомлення відправлено: ${data.status}`);
      setTo('');
      setMessage('');
    } catch (error) {
      console.error('Помилка відправки:', error);
      alert('Не вдалося відправити повідомлення');
    }
  };

  return (
    <form onSubmit={sendChat} className="mb-6 p-4 rounded shadow">
      <h2 className="text-xl font-semibold mb-2">Написати в чат</h2>
      
      <div className="mb-2">
        <label className="block">Канал</label>
        <select
          value={to}
          onChange={e => setTo(e.target.value)}
          className="border p-1 w-full bg-white"
          required
        >
          <option value="">Оберіть канал...</option>
          {channels.map(channel => (
            <option key={channel.id} value={channel.jid}>
              {channel.name} (ID: {channel.id})
            </option>
          ))}
        </select>
      </div>

      <div className="mb-4">
        <label className="block">Повідомлення</label>
        <textarea
          value={message}
          onChange={e => setMessage(e.target.value)}
          className="border p-1 w-full h-24"
          placeholder="Введіть текст повідомлення..."
          required
        />
      </div>

      <button 
        type="submit" 
        className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded"
      >
        Надіслати
      </button>
    </form>
  );
}