import React from 'react';

interface TrackInfoProps {
  trackName: string;
  artist: string;
}

const TrackInfo: React.FC<TrackInfoProps> = ({ trackName, artist }) => {
  return (
    <div className="text-white text-center">
      <h3 className="font-bold">{trackName}</h3>
      <p className="text-sm">{artist}</p>
    </div>
  );
};

export default TrackInfo;
