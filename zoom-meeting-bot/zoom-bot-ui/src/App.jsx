import MeetingList from './components/MeetingList';
import MeetingForm from './components/MeetingForm';
import ChatForm from './components/ChatForm';
import JoinMeeting from './components/JoinMeeting';

export default function App() {
  return (
    <div className="p-4 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Zoom Chat Bot Dashboard</h1>
      <MeetingForm />
      <MeetingList />
      <ChatForm />
      <JoinMeeting />
    </div>
  );
}